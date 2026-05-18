import json
from dataclasses import replace

from langgraph.graph import END, START, StateGraph

from app.agents.candidate_job_matcher import CandidateJobMatcherAgent
from app.agents.candidate_profiler import CandidateProfilerAgent
from app.agents.company_researcher import CompanyResearchAgent
from app.agents.interview_intel_collector import InterviewIntelAgent
from app.agents.interview_plan_critic import InterviewPlanCriticAgent
from app.agents.interview_planner import InterviewPlannerAgent
from app.agents.jd_analyzer import JDAnalyzerAgent
from app.agents.resume_extractor import ResumeExtractorAgent
from app.domain.models import (
    DocumentType,
    InterviewPlan,
    KnowledgeRetrievalResult,
    RetrievedKnowledgeChunk,
)
from app.graph.state import InterviewGraphState
from app.ports.tools import (
    ChunkingTool,
    DocumentParsingTool,
    KnowledgeBaseIndexer,
    KnowledgeRetrievalTool,
)
from app.skills.contracts import (
    CandidateJobMatchingSkill,
    CandidateProfilingSkill,
    CompanyResearchSkill,
    InterviewIntelSkill,
    InterviewPlanCriticSkill,
    JDAnalysisSkill,
    InterviewPlanningSkill,
    ResumeExtractionSkill,
)
from app.tools.knowledge_reranker import rerank_retrieved_chunks


class LangGraphInterviewWorkflow:
    PLANNING_RETRIEVAL_PREFETCH_K = 24
    PLANNING_RETRIEVAL_TOP_K_PER_QUERY = 12
    PLANNING_RETRIEVAL_FINAL_TOP_K = 12

    def __init__(
        self,
        document_parsing_tool: DocumentParsingTool | None = None,
        chunking_tool: ChunkingTool | None = None,
        resume_extraction_skill: ResumeExtractionSkill | None = None,
        candidate_profiling_skill: CandidateProfilingSkill | None = None,
        jd_analysis_skill: JDAnalysisSkill | None = None,
        candidate_job_matching_skill: CandidateJobMatchingSkill | None = None,
        company_research_skill: CompanyResearchSkill | None = None,
        interview_intel_skill: InterviewIntelSkill | None = None,
        interview_planning_skill: InterviewPlanningSkill | None = None,
        interview_plan_critic_skill: InterviewPlanCriticSkill | None = None,
        knowledge_base_indexer: KnowledgeBaseIndexer | None = None,
        knowledge_retrieval_tool: KnowledgeRetrievalTool | None = None,
    ) -> None:
        self.document_parsing_tool = document_parsing_tool
        self.chunking_tool = chunking_tool
        self.resume_extraction_skill = resume_extraction_skill
        self.candidate_profiling_skill = candidate_profiling_skill
        self.jd_analysis_skill = jd_analysis_skill
        self.candidate_job_matching_skill = candidate_job_matching_skill
        self.company_research_skill = company_research_skill
        self.interview_intel_skill = interview_intel_skill
        self.interview_planning_skill = interview_planning_skill
        self.interview_plan_critic_skill = interview_plan_critic_skill
        self.knowledge_base_indexer = knowledge_base_indexer
        self.knowledge_retrieval_tool = knowledge_retrieval_tool

    async def ingest_documents(self, state: InterviewGraphState) -> InterviewGraphState:
        if self.document_parsing_tool is None:
            return state

        parsed_documents = list(state.parsed_documents)
        document_chunks = list(state.document_chunks)

        for document_input in state.document_inputs:
            parsed_document = await self.document_parsing_tool.parse_document(
                file_path=document_input.file_path,
                document_type=document_input.document_type,
                document_id=document_input.document_id,
            )
            if document_input.document_type == DocumentType.KNOWLEDGE_BASE:
                parsed_document = replace(
                    parsed_document,
                    metadata={
                        **parsed_document.metadata,
                        "source_file_path": str(document_input.file_path.resolve()),
                    },
                )
                parsed_documents.append(parsed_document)
                continue

            parsed_documents.append(parsed_document)

            if self.chunking_tool is not None:
                chunks = await self.chunking_tool.chunk_document(parsed_document)
                document_chunks.extend(chunks)

        return replace(
            state,
            parsed_documents=parsed_documents,
            document_chunks=document_chunks,
        )

    async def index_knowledge_base(self, state: InterviewGraphState) -> InterviewGraphState:
        if self.knowledge_base_indexer is None:
            return state

        knowledge_documents = [
            document
            for document in state.parsed_documents
            if document.document_type == DocumentType.KNOWLEDGE_BASE
        ]
        if not knowledge_documents:
            return state

        indexing_result = await self.knowledge_base_indexer.index_documents(
            session_id=state.session_id,
            documents=knowledge_documents,
        )
        return replace(state, knowledge_indexing_result=indexing_result)

    async def extract_resume_profile(self, state: InterviewGraphState) -> InterviewGraphState:
        if self.resume_extraction_skill is None:
            return state

        parsed_resume = next(
            (
                document
                for document in state.parsed_documents
                if document.document_type == DocumentType.RESUME
            ),
            None,
        )
        if parsed_resume is None:
            raise ValueError("a parsed resume document is required before resume extraction")

        agent = ResumeExtractorAgent(
            user_id=state.user_id,
            parsed_resume=parsed_resume,
            resume_extraction_skill=self.resume_extraction_skill,
        )
        resume_profile = await agent.run()
        return replace(state, resume_profile=resume_profile)

    async def profile_candidate(self, state: InterviewGraphState) -> InterviewGraphState:
        if self.candidate_profiling_skill is None:
            return state

        if state.resume_profile is None:
            raise ValueError("resume_profile is required before candidate profiling")

        agent = CandidateProfilerAgent(
            user_id=state.user_id,
            session_id=state.session_id,
            resume_profile=state.resume_profile,
            candidate_profiling_skill=self.candidate_profiling_skill,
        )
        candidate_profile = await agent.run()
        return replace(state, candidate_profile=candidate_profile)

    async def analyze_jd(self, state: InterviewGraphState) -> InterviewGraphState:
        if self.jd_analysis_skill is None:
            return state

        agent = JDAnalyzerAgent(
            session_id=state.session_id,
            company_name=state.company_name,
            role_title=state.role_title,
            jd_text=state.jd_text,
            jd_analysis_skill=self.jd_analysis_skill,
        )
        job_analysis = await agent.run()
        return replace(state, job_analysis=job_analysis)

    async def match_candidate_to_job(self, state: InterviewGraphState) -> InterviewGraphState:
        if self.candidate_job_matching_skill is None:
            return state

        if state.candidate_profile is None:
            raise ValueError("candidate_profile is required before candidate-job matching")
        if state.job_analysis is None:
            raise ValueError("job_analysis is required before candidate-job matching")

        agent = CandidateJobMatcherAgent(
            session_id=state.session_id,
            candidate_profile=state.candidate_profile,
            job_analysis=state.job_analysis,
            candidate_job_matching_skill=self.candidate_job_matching_skill,
        )
        candidate_job_match = await agent.run()
        return replace(state, candidate_job_match=candidate_job_match)

    async def research_company(self, state: InterviewGraphState) -> InterviewGraphState:
        if self.company_research_skill is None:
            return state

        if state.job_analysis is None:
            raise ValueError("job_analysis is required before company research")

        agent = CompanyResearchAgent(
            company_name=state.company_name,
            role_title=state.role_title,
            job_analysis=state.job_analysis,
            company_research_skill=self.company_research_skill,
        )
        company_sources = await agent.run()
        return replace(state, company_sources=company_sources)

    async def collect_interview_intel(self, state: InterviewGraphState) -> InterviewGraphState:
        if self.interview_intel_skill is None:
            return state

        topics = self._build_interview_intel_topics(state)
        agent = InterviewIntelAgent(
            company_name=state.company_name,
            role_title=state.role_title,
            topics=topics,
            interview_intel_skill=self.interview_intel_skill,
        )
        interview_intel = await agent.run()
        return replace(state, interview_intel=interview_intel)

    def _build_interview_intel_topics(self, state: InterviewGraphState) -> list[str]:
        topics: list[str] = []

        if state.job_analysis is not None:
            topics.extend(state.job_analysis.required_skills)
            topics.extend(state.job_analysis.preferred_skills)

        if state.candidate_profile is not None:
            topics.extend(state.candidate_profile.technical_skills)
            topics.extend(state.candidate_profile.follow_up_targets)

        if state.candidate_job_match is not None:
            topics.extend(state.candidate_job_match.role_specific_risk_areas)

        return list(dict.fromkeys(topic for topic in topics if topic.strip()))[:12]

    async def retrieve_planning_context(self, state: InterviewGraphState) -> InterviewGraphState:
        if self.knowledge_retrieval_tool is None:
            return state
        if state.knowledge_indexing_result is None:
            return state

        query_map = self._build_planning_retrieval_queries(state)
        if not query_map:
            return state

        retrieval_results: list[KnowledgeRetrievalResult] = []
        retrieval_debug_rows: list[str] = []
        for query_name, query_text in query_map.items():
            result = await self.knowledge_retrieval_tool.retrieve_knowledge(
                session_id=state.session_id,
                query=query_text,
                top_k=self.PLANNING_RETRIEVAL_TOP_K_PER_QUERY,
                prefetch_k=self.PLANNING_RETRIEVAL_PREFETCH_K,
                document_types=[DocumentType.KNOWLEDGE_BASE],
            )
            retrieval_debug_rows.append(
                f"planning_retrieval.query={query_name} hits={len(result.chunks)}"
            )
            result = self._tag_retrieval_query(result=result, query_name=query_name)
            retrieval_results.append(result)

        planning_knowledge_context = self._merge_planning_retrieval_results(
            session_id=state.session_id,
            retrieval_results=retrieval_results,
            retrieval_debug_rows=retrieval_debug_rows,
        )
        return replace(state, planning_knowledge_context=planning_knowledge_context)

    def _build_planning_retrieval_queries(self, state: InterviewGraphState) -> dict[str, str]:
        common_parts: list[str] = []
        common_parts.append(f"Company: {state.company_name}")
        common_parts.append(f"Role title: {state.role_title}")
        common_parts.append(f"Target track: {state.target_track}")
        common_parts.append(f"JD text:\n{state.jd_text}")

        if state.job_analysis is not None:
            common_parts.append("JD required skills: " + ", ".join(state.job_analysis.required_skills))
            common_parts.append("JD preferred skills: " + ", ".join(state.job_analysis.preferred_skills))
            common_parts.append("JD responsibilities: " + ", ".join(state.job_analysis.responsibilities))

        if state.candidate_profile is not None:
            common_parts.append(
                "Candidate technical skills: " + ", ".join(state.candidate_profile.technical_skills)
            )
            common_parts.append(
                "Candidate project highlights: " + ", ".join(state.candidate_profile.project_highlights)
            )
            common_parts.append(
                "Candidate follow-up targets: " + ", ".join(state.candidate_profile.follow_up_targets)
            )

        if state.candidate_job_match is not None:
            common_parts.append(
                "Candidate-job matches: " + ", ".join(state.candidate_job_match.candidate_matches)
            )
            common_parts.append(
                "Role-specific risk areas: "
                + ", ".join(state.candidate_job_match.role_specific_risk_areas)
            )

        common_context = "\n".join(part for part in common_parts if part.strip())
        if not common_context:
            return {}

        queries: dict[str, str] = {}
        queries["project_deep_dive"] = (
            "Retrieval intent: project deep dive evidence for written and implied projects.\n"
            + common_context
        )
        queries["tech_deep_dive"] = (
            "Retrieval intent: technical deep dive evidence for stack-level questions.\n"
            + common_context
        )
        queries["scenario"] = (
            "Retrieval intent: scenario question evidence for JD constraints and production tradeoffs.\n"
            + common_context
        )
        return queries

    def _merge_planning_retrieval_results(
        self,
        session_id,
        retrieval_results: list[KnowledgeRetrievalResult],
        retrieval_debug_rows: list[str],
    ) -> KnowledgeRetrievalResult:
        chunk_by_id: dict[str, RetrievedKnowledgeChunk] = {}
        chunk_hit_counts: dict[str, int] = {}
        warnings: list[str] = []
        total_candidates = 0

        for result in retrieval_results:
            warnings.extend(result.warnings)
            for chunk in result.chunks:
                total_candidates += 1
                chunk_id = str(chunk.chunk.id)
                if chunk_id not in chunk_hit_counts:
                    chunk_hit_counts[chunk_id] = 0
                chunk_hit_counts[chunk_id] += 1
                if chunk_id not in chunk_by_id:
                    chunk_by_id[chunk_id] = chunk
                    continue
                existing_chunk = chunk_by_id[chunk_id]
                if chunk.score > existing_chunk.score:
                    chunk_by_id[chunk_id] = chunk

        merged_chunks = list(chunk_by_id.values())
        pre_rerank_top5 = [str(item.chunk.id) for item in merged_chunks[:5]]
        merged_chunks.sort(
            key=lambda item: (
                item.score,
                chunk_hit_counts.get(str(item.chunk.id), 0),
            ),
            reverse=True,
        )
        pre_rerank_sorted_top5 = [str(item.chunk.id) for item in merged_chunks[:5]]

        # Stage-2 rerank: cross-encoder reranks the merged candidate pool.
        merged_query = " ".join(
            [
                "project deep dive evidence",
                "tech stack deep dive evidence",
                "jd scenario evidence",
            ]
        )
        if len(merged_chunks) > 1:
            merged_chunks = rerank_retrieved_chunks(merged_query, merged_chunks)
        post_rerank_top5 = [str(item.chunk.id) for item in merged_chunks[:5]]

        merged_chunks = merged_chunks[: self.PLANNING_RETRIEVAL_FINAL_TOP_K]

        reranked_chunks: list[RetrievedKnowledgeChunk] = []
        for index, chunk in enumerate(merged_chunks, start=1):
            reranked_chunks.append(
                RetrievedKnowledgeChunk(
                    chunk=chunk.chunk,
                    score=chunk.score,
                    rank=index,
                    retrieval_query=chunk.retrieval_query,
                )
            )

        merged_query = "MULTI_QUERY(project_deep_dive, tech_deep_dive, scenario)+RERANK"
        warnings.extend(retrieval_debug_rows)
        warnings.append(f"planning_retrieval.total_candidates={total_candidates}")
        warnings.append(f"planning_retrieval.unique_candidates={len(chunk_by_id)}")
        warnings.append(f"planning_retrieval.prefilter_top5={pre_rerank_top5}")
        warnings.append(f"planning_retrieval.presort_top5={pre_rerank_sorted_top5}")
        warnings.append(f"planning_retrieval.rerank_top5={post_rerank_top5}")
        warnings.append(
            f"planning_retrieval.final_top_k={self.PLANNING_RETRIEVAL_FINAL_TOP_K}"
        )
        return KnowledgeRetrievalResult(
            session_id=session_id,
            query=merged_query,
            chunks=reranked_chunks,
            warnings=warnings,
        )

    def _tag_retrieval_query(
        self,
        result: KnowledgeRetrievalResult,
        query_name: str,
    ) -> KnowledgeRetrievalResult:
        tagged_chunks: list[RetrievedKnowledgeChunk] = []
        for chunk in result.chunks:
            tagged_chunks.append(
                RetrievedKnowledgeChunk(
                    chunk=chunk.chunk,
                    score=chunk.score,
                    rank=chunk.rank,
                    retrieval_query=f"{query_name}:{chunk.retrieval_query}",
                )
            )
        return KnowledgeRetrievalResult(
            session_id=result.session_id,
            query=f"{query_name}:{result.query}",
            chunks=tagged_chunks,
            warnings=result.warnings,
        )

    async def plan_interview(self, state: InterviewGraphState) -> InterviewGraphState:
        if self.interview_planning_skill is None:
            return state

        if state.candidate_profile is None:
            raise ValueError("candidate_profile is required before planning an interview")
        if state.job_analysis is None:
            raise ValueError("job_analysis is required before planning an interview")
        if state.candidate_job_match is None:
            raise ValueError("candidate_job_match is required before planning an interview")

        agent = InterviewPlannerAgent(
            session_id=state.session_id,
            target_track=state.target_track,
            candidate_profile=state.candidate_profile,
            job_analysis=state.job_analysis,
            candidate_job_match=state.candidate_job_match,
            company_sources=state.company_sources,
            interview_intel=state.interview_intel,
            interview_planning_skill=self.interview_planning_skill,
            knowledge_context=state.planning_knowledge_context,
            reusable_question_memories=state.reusable_question_memories,
            previous_plan_critique=state.interview_plan_critique,
        )
        interview_plan = await agent.run()
        interview_plan = self._attach_planner_revision_metadata(
            interview_plan=interview_plan,
            planner_revision_attempts=state.planner_revision_attempts,
            state=state,
        )
        return replace(state, interview_plan=interview_plan)

    def _attach_planner_revision_metadata(
        self,
        interview_plan: InterviewPlan,
        planner_revision_attempts: int,
        state: InterviewGraphState,
    ) -> InterviewPlan:
        updated_rubric = dict(interview_plan.rubric)
        closure_event = {
            "event_name": "resume_to_questions_closure",
            "session_id": str(state.session_id),
            "resume_document_count": len(
                [
                    d
                    for d in state.parsed_documents
                    if d.document_type == DocumentType.RESUME
                ]
            ),
            "knowledge_base_document_count": len(
                [
                    d
                    for d in state.parsed_documents
                    if d.document_type == DocumentType.KNOWLEDGE_BASE
                ]
            ),
            "candidate_skill_count": (
                len(state.candidate_profile.technical_skills)
                if state.candidate_profile is not None
                else 0
            ),
            "retrieved_chunk_count": (
                len(state.planning_knowledge_context.chunks)
                if state.planning_knowledge_context is not None
                else 0
            ),
            "reusable_question_memory_count": len(state.reusable_question_memories),
            "question_count": len(interview_plan.questions),
            "revised": planner_revision_attempts > 0,
            "revision_attempts_used": planner_revision_attempts,
            "target_track": state.target_track,
        }
        updated_rubric["observability_event.resume_to_questions_closure"] = json.dumps(
            closure_event,
            ensure_ascii=False,
        )

        return InterviewPlan(
            session_id=interview_plan.session_id,
            mode=interview_plan.mode,
            questions=interview_plan.questions,
            rubric=updated_rubric,
            candidate_storyline=interview_plan.candidate_storyline,
            planned_deep_dives=interview_plan.planned_deep_dives,
            target_track=interview_plan.target_track,
            revised=planner_revision_attempts > 0,
            revision_attempts_used=planner_revision_attempts,
        )

    async def critique_interview_plan(self, state: InterviewGraphState) -> InterviewGraphState:
        if self.interview_plan_critic_skill is None:
            return state

        if state.interview_plan is None:
            raise ValueError("interview_plan is required before critique")
        if state.candidate_profile is None:
            raise ValueError("candidate_profile is required before critique")
        if state.job_analysis is None:
            raise ValueError("job_analysis is required before critique")
        if state.candidate_job_match is None:
            raise ValueError("candidate_job_match is required before critique")

        agent = InterviewPlanCriticAgent(
            session_id=state.session_id,
            interview_plan=state.interview_plan,
            candidate_profile=state.candidate_profile,
            job_analysis=state.job_analysis,
            candidate_job_match=state.candidate_job_match,
            interview_plan_critic_skill=self.interview_plan_critic_skill,
            knowledge_context=state.planning_knowledge_context,
        )
        interview_plan_critique = await agent.run()
        return replace(state, interview_plan_critique=interview_plan_critique)

    async def prepare_planner_revision(self, state: InterviewGraphState) -> InterviewGraphState:
        return replace(state, planner_revision_attempts=state.planner_revision_attempts + 1)

    def _route_after_critique(self, state: InterviewGraphState) -> str:
        if state.interview_plan_critique is None:
            return "finish"
        if state.interview_plan_critique.quality_gate_passed:
            return "finish"
        if state.planner_revision_attempts >= state.planner_max_revision_attempts:
            return "finish"
        return "revise"

    async def prepare_candidate_branch(self, state: InterviewGraphState) -> dict:
        candidate_state = await self.extract_resume_profile(state)
        candidate_state = await self.profile_candidate(candidate_state)
        return {
            "resume_profile": candidate_state.resume_profile,
            "candidate_profile": candidate_state.candidate_profile,
        }

    async def prepare_role_branch(self, state: InterviewGraphState) -> dict:
        role_state = await self.analyze_jd(state)
        role_state = await self.research_company(role_state)
        return {
            "job_analysis": role_state.job_analysis,
            "company_sources": role_state.company_sources,
        }

    async def prepare_knowledge_branch(self, state: InterviewGraphState) -> dict:
        knowledge_state = await self.index_knowledge_base(state)
        return {
            "knowledge_indexing_result": knowledge_state.knowledge_indexing_result,
        }

    async def run_live_turn(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def evaluate_session(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def generate_report(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    def build_preparation_graph(self):
        graph = StateGraph(InterviewGraphState)

        graph.add_node("ingest_documents", self.ingest_documents)
        graph.add_node("prepare_candidate_branch", self.prepare_candidate_branch)
        graph.add_node("prepare_role_branch", self.prepare_role_branch)
        graph.add_node("prepare_knowledge_branch", self.prepare_knowledge_branch)
        graph.add_node("match_candidate_to_job", self.match_candidate_to_job)
        graph.add_node("collect_interview_intel", self.collect_interview_intel)
        graph.add_node("retrieve_planning_context", self.retrieve_planning_context)
        graph.add_node("plan_interview", self.plan_interview)
        graph.add_node("critique_interview_plan", self.critique_interview_plan)
        graph.add_node("prepare_planner_revision", self.prepare_planner_revision)

        graph.add_edge(START, "ingest_documents")
        graph.add_edge("ingest_documents", "prepare_candidate_branch")
        graph.add_edge("ingest_documents", "prepare_role_branch")
        graph.add_edge("ingest_documents", "prepare_knowledge_branch")
        graph.add_edge(
            ["prepare_candidate_branch", "prepare_role_branch"],
            "match_candidate_to_job",
        )
        graph.add_edge("match_candidate_to_job", "collect_interview_intel")
        graph.add_edge(
            ["prepare_knowledge_branch", "collect_interview_intel"],
            "retrieve_planning_context",
        )
        graph.add_edge("retrieve_planning_context", "plan_interview")
        graph.add_edge("plan_interview", "critique_interview_plan")
        graph.add_conditional_edges(
            "critique_interview_plan",
            self._route_after_critique,
            {
                "revise": "prepare_planner_revision",
                "finish": END,
            },
        )
        graph.add_edge("prepare_planner_revision", "plan_interview")

        return graph.compile()

    def build_live_interview_graph(self, checkpointer=None):
        graph = StateGraph(InterviewGraphState)

        graph.add_node("run_live_turn", self.run_live_turn)
        graph.add_node("evaluate_session", self.evaluate_session)
        graph.add_node("generate_report", self.generate_report)

        graph.add_edge(START, "run_live_turn")
        graph.add_edge("run_live_turn", "evaluate_session")
        graph.add_edge("evaluate_session", "generate_report")
        graph.add_edge("generate_report", END)

        return graph.compile(checkpointer=checkpointer)
