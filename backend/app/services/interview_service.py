from pathlib import Path
from uuid import UUID

from app.agents.evaluator import EvaluatorAgent
from app.agents.live_interviewer import LiveInterviewerAgent
from app.agents.report_generator import ReportGeneratorAgent
from app.config.settings import load_settings
from app.db.session import build_async_engine, build_session_factory, session_scope
from app.domain.models import (
    AnswerEvaluation,
    DocumentInput,
    DocumentType,
    InterviewMode,
    InterviewPlan,
    InterviewQuestion,
    InterviewTurn,
    InterviewTurnRole,
    MemoryKind,
)
from app.graph.langgraph_workflow import LangGraphInterviewWorkflow
from app.graph.state import InterviewGraphState
from app.ports.memory import LongTermMemoryRepository
from app.ports.tools import VectorStore
from app.providers.embeddings import OpenAIEmbeddingProvider
from app.providers.llm import build_chat_model
from app.services.long_term_memory_store import LongTermMemoryStore
from app.services.memory_service import MemoryNamespaceFactory, build_memory_record
from app.services.postgres_persistence import OptionalPostgresPersistence
from app.services.short_term_memory import (
    build_short_term_memory_config,
    postgres_short_term_checkpointer,
)
from app.services.session_store import InterviewSessionRecord, InMemoryInterviewSessionStore
from app.skills.candidate_job_matching import LLMCandidateJobMatchingSkill
from app.skills.candidate_profiling import LLMCandidateProfilingSkill
from app.skills.company_research import LLMCompanyResearchSkill
from app.skills.evaluation import LLMAnswerEvaluationSkill
from app.skills.interview_intel import LLMInterviewIntelSkill
from app.skills.interview_plan_critic import LLMInterviewPlanCriticSkill
from app.skills.interview_planning import LLMInterviewPlanningSkill
from app.skills.jd_analysis import LLMJDAnalysisSkill
from app.skills.live_interview import LLMLiveInterviewSkill
from app.skills.report_generation import LLMReportGenerationSkill
from app.skills.resume_extraction import LLMResumeExtractionSkill
from app.tools.chunking import RecursiveTextChunkingTool
from app.tools.document_parsing import LocalDocumentParsingTool
from app.tools.faiss_vector_store import FaissVectorStore, get_process_faiss_vector_store
from app.tools.in_memory_vector_store import InMemoryVectorStore
from app.tools.knowledge_retrieval import DefaultKnowledgeRetrievalTool
from app.tools.mock_research import MockPageFetchTool, MockWebSearchTool
from app.tools.postgres_vector_store import PostgresVectorStore
from app.tools.windowed_knowledge_indexer import WindowedKnowledgeBaseIndexer
from app.utils.serialization import to_jsonable


class InterviewService:
    def __init__(
        self,
        store: InMemoryInterviewSessionStore,
        *,
        shared_faiss_vector_store: FaissVectorStore | None = None,
        long_term_memory_repository: LongTermMemoryRepository | None = None,
        memory_namespace_factory: MemoryNamespaceFactory | None = None,
    ) -> None:
        settings = load_settings()
        self.store = store
        self.persistence = OptionalPostgresPersistence(settings)
        self._shared_faiss_vector_store = shared_faiss_vector_store
        self.long_term_memory_repository = (
            long_term_memory_repository or LongTermMemoryStore(settings)
        )
        self.memory_namespace_factory = (
            memory_namespace_factory or MemoryNamespaceFactory()
        )

    async def create_session(
        self,
        company_name: str,
        role_title: str,
        target_track: str,
        jd_text: str,
        mode: InterviewMode = InterviewMode.GENERAL_SWE,
    ) -> InterviewSessionRecord:
        session = self.store.create_session(
            company_name=company_name,
            role_title=role_title,
            target_track=target_track,
            jd_text=jd_text,
            mode=mode,
        )
        await self.persistence.persist_session(session)
        return session

    async def add_document(
        self,
        session_id: UUID,
        file_path: Path,
        document_type: DocumentType,
    ) -> DocumentInput:
        session = self.store.require_session(session_id)
        document_input = DocumentInput(file_path=file_path, document_type=document_type)
        session.document_inputs.append(document_input)
        await self.persistence.persist_uploaded_document(session, document_input)
        return document_input

    async def add_documents_from_path(
        self,
        session_id: UUID,
        root_path: Path,
        document_type: DocumentType,
        suffixes: set[str] | None = None,
    ) -> list[DocumentInput]:
        session = self.store.require_session(session_id)
        supported_suffixes = suffixes or {".pdf"}
        document_inputs: list[DocumentInput] = []

        for file_path in _iter_document_paths(root_path, supported_suffixes):
            document_input = DocumentInput(
                file_path=file_path,
                document_type=document_type,
            )
            session.document_inputs.append(document_input)
            await self.persistence.persist_uploaded_document(session, document_input)
            document_inputs.append(document_input)

        return document_inputs

    async def prepare_session(self, session_id: UUID) -> InterviewPlan:
        session = self.store.require_session(session_id)
        settings = load_settings()
        llm = build_chat_model(settings)
        chunking_tool = RecursiveTextChunkingTool()

        if settings.vector_store_backend == "postgres":
            if not settings.database_url:
                raise ValueError(
                    "VECTOR_STORE_BACKEND=postgres requires DATABASE_URL to be set."
                )

            engine = build_async_engine(settings.database_url)
            try:
                session_factory = build_session_factory(engine)
                async for db_session in session_scope(session_factory):
                    vector_store = PostgresVectorStore(db_session)
                    prepared_state = await self._run_preparation_workflow(
                        session=session,
                        llm=llm,
                        chunking_tool=chunking_tool,
                        vector_store=vector_store,
                    )
            finally:
                await engine.dispose()
        elif settings.vector_store_backend == "faiss":
            faiss_store = self._shared_faiss_vector_store or get_process_faiss_vector_store(
                persist_directory=settings.faiss_persist_directory,
                allow_local_index_pickles=settings.faiss_allow_local_index_pickles,
            )
            prepared_state = await self._run_preparation_workflow(
                session=session,
                llm=llm,
                chunking_tool=chunking_tool,
                vector_store=faiss_store,
            )
        else:
            prepared_state = await self._run_preparation_workflow(
                session=session,
                llm=llm,
                chunking_tool=chunking_tool,
                vector_store=InMemoryVectorStore(),
            )

        interview_plan = prepared_state["interview_plan"]
        if interview_plan is None:
            raise ValueError("Preparation graph did not create an interview plan")

        session.prepared_state = prepared_state
        session.interview_plan = interview_plan
        await self.persistence.persist_prepared_session(session)
        await self._save_interview_plan_to_long_term_memory(
            session=session,
            interview_plan=interview_plan,
            prepared_state=prepared_state,
        )
        return interview_plan

    async def _run_preparation_workflow(
        self,
        session: InterviewSessionRecord,
        llm,
        chunking_tool: RecursiveTextChunkingTool,
        vector_store: VectorStore,
    ) -> InterviewGraphState:
        settings = load_settings()
        if settings.openai_api_key is None:
            raise ValueError("OPENAI_API_KEY is required to run RAG preparation")

        embedding_provider = OpenAIEmbeddingProvider(api_key=settings.openai_api_key)
        mock_web_search_tool = MockWebSearchTool()
        mock_page_fetch_tool = MockPageFetchTool()

        document_parsing_tool = LocalDocumentParsingTool()

        workflow = LangGraphInterviewWorkflow(
            document_parsing_tool=document_parsing_tool,
            chunking_tool=chunking_tool,
            resume_extraction_skill=LLMResumeExtractionSkill(llm),
            candidate_profiling_skill=LLMCandidateProfilingSkill(llm),
            jd_analysis_skill=LLMJDAnalysisSkill(llm),
            candidate_job_matching_skill=LLMCandidateJobMatchingSkill(llm),
            company_research_skill=LLMCompanyResearchSkill(
                llm=llm,
                web_search_tool=mock_web_search_tool,
                page_fetch_tool=mock_page_fetch_tool,
            ),
            interview_intel_skill=LLMInterviewIntelSkill(
                llm=llm,
                web_search_tool=mock_web_search_tool,
                page_fetch_tool=mock_page_fetch_tool,
            ),
            interview_planning_skill=LLMInterviewPlanningSkill(llm),
            interview_plan_critic_skill=LLMInterviewPlanCriticSkill(llm),
            knowledge_base_indexer=WindowedKnowledgeBaseIndexer(
                document_parser=document_parsing_tool,
                chunking_tool=chunking_tool,
                embedding_provider=embedding_provider,
                vector_store=vector_store,
            ),
            knowledge_retrieval_tool=DefaultKnowledgeRetrievalTool(
                embedding_provider=embedding_provider,
                vector_store=vector_store,
            ),
        )

        initial_state = InterviewGraphState(
            session_id=session.session_id,
            user_id=session.user_id,
            company_name=session.company_name,
            role_title=session.role_title,
            target_track=session.target_track,
            jd_text=session.jd_text,
            document_inputs=session.document_inputs,
            reusable_question_memories=await self._load_reusable_question_memories(
                session
            ),
        )
        runnable = workflow.build_preparation_graph()
        if not settings.langsmith_tracing:
            return await runnable.ainvoke(initial_state)

        try:
            from langchain_core.tracers.langchain import LangChainTracer
        except ImportError:
            return await runnable.ainvoke(initial_state)

        tracer = LangChainTracer(project_name=settings.langsmith_project)
        config = {
            "callbacks": [tracer],
            "tags": ["prepare_session", "planner", "rag"],
            "metadata": {
                "session_id": str(session.session_id),
                "company_name": session.company_name,
                "role_title": session.role_title,
                "target_track": session.target_track,
                "vector_store_backend": settings.vector_store_backend,
            },
        }
        return await runnable.ainvoke(initial_state, config=config)

    def get_interview_plan(self, session_id: UUID) -> InterviewPlan:
        session = self.store.require_session(session_id)
        if session.interview_plan is None:
            raise ValueError("Interview session has not been prepared")
        return session.interview_plan

    async def get_interview_plan_payload(self, session_id: UUID) -> dict:
        try:
            return to_jsonable(self.get_interview_plan(session_id))
        except (KeyError, ValueError):
            plan_payload = await self.persistence.get_interview_plan_payload(session_id)
            if plan_payload is None:
                raise ValueError("Interview session has not been prepared")
            return plan_payload

    async def submit_answer(
        self,
        session_id: UUID,
        question_id: UUID,
        answer: str,
    ) -> InterviewQuestion | None:
        session = self.store.require_session(session_id)
        plan = self._require_plan(session)
        question = self._find_question(plan, question_id)

        if not self._has_interviewer_turn(session, question_id):
            session.transcript.append(
                InterviewTurn(
                    session_id=session.session_id,
                    role=InterviewTurnRole.INTERVIEWER,
                    content=question.prompt,
                    metadata={"question_id": str(question.id)},
                )
            )

        session.transcript.append(
            InterviewTurn(
                session_id=session.session_id,
                role=InterviewTurnRole.CANDIDATE,
                content=answer,
                metadata={"question_id": str(question.id)},
            )
        )

        settings = load_settings()
        llm = build_chat_model(settings)
        live_agent = LiveInterviewerAgent(
            session_id=session.session_id,
            plan=plan,
            transcript=session.transcript,
            live_interview_skill=LLMLiveInterviewSkill(llm),
        )
        follow_up = await live_agent.decide_follow_up(
            current_question=question,
            candidate_answer=answer,
        )
        await self.persistence.persist_transcript(session)
        await self._checkpoint_live_interview_state(session)
        return follow_up

    async def evaluate_session(self, session_id: UUID) -> list[AnswerEvaluation]:
        session = self.store.require_session(session_id)
        plan = self._require_plan(session)
        settings = load_settings()
        llm = build_chat_model(settings)
        evaluations: list[AnswerEvaluation] = []

        for turn in session.transcript:
            if turn.role != InterviewTurnRole.CANDIDATE:
                continue

            question_id = turn.metadata.get("question_id")
            if question_id is None:
                continue

            question = self._find_question(plan, UUID(str(question_id)))
            evaluator = EvaluatorAgent(
                session_id=session.session_id,
                question=question,
                candidate_answer=turn.content,
                evaluation_skill=LLMAnswerEvaluationSkill(llm),
            )
            evaluations.append(await evaluator.run())

        session.evaluations = evaluations
        await self.persistence.persist_evaluations(session)
        return evaluations

    async def generate_report(self, session_id: UUID) -> str:
        session = self.store.require_session(session_id)
        if not session.evaluations:
            await self.evaluate_session(session_id)

        settings = load_settings()
        llm = build_chat_model(settings)
        reporter = ReportGeneratorAgent(
            session_id=session.session_id,
            transcript=session.transcript,
            evaluations=session.evaluations,
            report_generation_skill=LLMReportGenerationSkill(llm),
        )
        session.report = await reporter.run()
        await self.persistence.persist_report(session)
        return session.report

    def get_report(self, session_id: UUID) -> str:
        session = self.store.require_session(session_id)
        if session.report is None:
            raise ValueError("Report has not been generated")
        return session.report

    def _require_plan(self, session: InterviewSessionRecord) -> InterviewPlan:
        if session.interview_plan is None:
            raise ValueError("Interview session has not been prepared")
        return session.interview_plan

    def _find_question(self, plan: InterviewPlan, question_id: UUID) -> InterviewQuestion:
        for question in plan.questions:
            if question.id == question_id:
                return question
        raise ValueError(f"Question not found in interview plan: {question_id}")

    def _has_interviewer_turn(
        self,
        session: InterviewSessionRecord,
        question_id: UUID,
    ) -> bool:
        return any(
            turn.role == InterviewTurnRole.INTERVIEWER
            and turn.metadata.get("question_id") == str(question_id)
            for turn in session.transcript
        )

    async def _save_interview_plan_to_long_term_memory(
        self,
        session: InterviewSessionRecord,
        interview_plan: InterviewPlan,
        prepared_state,
    ) -> None:
        namespace = self.memory_namespace_factory.shared_question_bank(
            target_track=session.target_track,
            company_name=session.company_name,
            role_title=session.role_title,
            jd_text=session.jd_text,
        )
        quality_scores = _question_quality_scores(prepared_state)
        memories = [
            build_memory_record(
                namespace=namespace,
                kind=MemoryKind.QUESTION_BANK,
                content={
                    "question_id": str(question.id),
                    "prompt": question.prompt,
                    "topic": question.topic,
                    "difficulty": question.difficulty,
                    "expected_signals": question.expected_signals,
                    "follow_up_strategy": question.follow_up_strategy,
                    "why_asked": question.why_asked,
                },
                metadata={
                    "company_name": session.company_name,
                    "role_title": session.role_title,
                    "target_track": session.target_track,
                    "question_type": (
                        question.question_type.value
                        if question.question_type is not None
                        else None
                    ),
                    "source_scope": (
                        question.source_scope.value
                        if question.source_scope is not None
                        else None
                    ),
                    "revised": interview_plan.revised,
                    "revision_attempts_used": interview_plan.revision_attempts_used,
                },
                source_session_id=session.session_id,
                source_user_id=session.user_id,
                quality_score=quality_scores.get(question.id),
            )
            for question in interview_plan.questions
        ]
        await self.long_term_memory_repository.save_memories(memories)

    async def _load_reusable_question_memories(
        self,
        session: InterviewSessionRecord,
    ):
        namespace = self.memory_namespace_factory.shared_question_bank(
            target_track=session.target_track,
            company_name=session.company_name,
            role_title=session.role_title,
            jd_text=session.jd_text,
        )
        return await self.long_term_memory_repository.list_memories(
            namespace=namespace,
            kind=MemoryKind.QUESTION_BANK,
            limit=8,
        )

    async def _checkpoint_live_interview_state(
        self,
        session: InterviewSessionRecord,
    ) -> None:
        state = InterviewGraphState(
            session_id=session.session_id,
            user_id=session.user_id,
            company_name=session.company_name,
            role_title=session.role_title,
            target_track=session.target_track,
            jd_text=session.jd_text,
            document_inputs=session.document_inputs,
            interview_plan=session.interview_plan,
            transcript=session.transcript,
        )
        workflow = LangGraphInterviewWorkflow()
        settings = load_settings()
        if settings.database_url is None:
            raise ValueError("DATABASE_URL is required for short-term memory")

        async with postgres_short_term_checkpointer(
            settings.database_url,
        ) as checkpointer:
            graph = workflow.build_live_interview_graph(checkpointer=checkpointer)
            await graph.ainvoke(
                state,
                config=build_short_term_memory_config(session),
            )


def _iter_document_paths(root_path: Path, suffixes: set[str]) -> list[Path]:
    normalized_suffixes = {suffix.lower() for suffix in suffixes}

    if root_path.is_file():
        return [root_path] if root_path.suffix.lower() in normalized_suffixes else []

    return sorted(
        path
        for path in root_path.rglob("*")
        if path.is_file() and path.suffix.lower() in normalized_suffixes
    )


def _question_quality_scores(prepared_state) -> dict[UUID, float]:
    critique = prepared_state.get("interview_plan_critique")
    if critique is None:
        return {}

    return {
        question_critique.question_id: question_critique.overall_score
        for question_critique in critique.question_critiques
    }
