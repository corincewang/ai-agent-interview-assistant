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
)
from app.graph.langgraph_workflow import LangGraphInterviewWorkflow
from app.graph.state import InterviewGraphState
from app.ports.tools import VectorStore
from app.providers.embeddings import OpenAIEmbeddingProvider
from app.providers.llm import build_chat_model
from app.services.postgres_persistence import OptionalPostgresPersistence
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
from app.tools.in_memory_vector_store import InMemoryVectorStore
from app.tools.knowledge_base_indexer import DefaultKnowledgeBaseIndexer
from app.tools.knowledge_retrieval import DefaultKnowledgeRetrievalTool
from app.tools.mock_research import MockPageFetchTool, MockWebSearchTool
from app.tools.postgres_vector_store import PostgresVectorStore
from app.utils.serialization import to_jsonable


class InterviewService:
    def __init__(self, store: InMemoryInterviewSessionStore) -> None:
        self.store = store
        self.persistence = OptionalPostgresPersistence(load_settings())

    async def create_session(
        self,
        company_name: str,
        role_title: str,
        jd_text: str,
        mode: InterviewMode,
    ) -> InterviewSessionRecord:
        session = self.store.create_session(
            company_name=company_name,
            role_title=role_title,
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

    async def prepare_session(self, session_id: UUID) -> InterviewPlan:
        session = self.store.require_session(session_id)
        settings = load_settings()
        llm = build_chat_model(settings)
        chunking_tool = RecursiveTextChunkingTool()

        if settings.database_url is not None:
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

        workflow = LangGraphInterviewWorkflow(
            document_parsing_tool=LocalDocumentParsingTool(),
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
            knowledge_base_indexer=DefaultKnowledgeBaseIndexer(
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
            jd_text=session.jd_text,
            document_inputs=session.document_inputs,
        )
        return await workflow.build_preparation_graph().ainvoke(initial_state)

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
