from dataclasses import replace

from langgraph.graph import END, START, StateGraph

from app.agents.candidate_job_matcher import CandidateJobMatcherAgent
from app.agents.candidate_profiler import CandidateProfilerAgent
from app.agents.company_researcher import CompanyResearchAgent
from app.agents.interview_intel_collector import InterviewIntelAgent
from app.agents.interview_planner import InterviewPlannerAgent
from app.agents.jd_analyzer import JDAnalyzerAgent
from app.agents.resume_extractor import ResumeExtractorAgent
from app.domain.models import DocumentType
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
    JDAnalysisSkill,
    InterviewPlanningSkill,
    ResumeExtractionSkill,
)


class LangGraphInterviewWorkflow:
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
            )
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

        query = self._build_planning_retrieval_query(state)
        if not query:
            return state

        planning_knowledge_context = await self.knowledge_retrieval_tool.retrieve_knowledge(
            session_id=state.session_id,
            query=query,
            top_k=5,
            document_types=[DocumentType.KNOWLEDGE_BASE],
        )
        return replace(state, planning_knowledge_context=planning_knowledge_context)

    def _build_planning_retrieval_query(self, state: InterviewGraphState) -> str:
        query_parts = [
            state.company_name,
            state.role_title,
            state.jd_text,
        ]

        if state.job_analysis is not None:
            query_parts.extend(state.job_analysis.required_skills)
            query_parts.extend(state.job_analysis.preferred_skills)

        if state.candidate_profile is not None:
            query_parts.extend(state.candidate_profile.technical_skills)
            query_parts.extend(state.candidate_profile.follow_up_targets)

        if state.candidate_job_match is not None:
            query_parts.extend(state.candidate_job_match.candidate_matches)
            query_parts.extend(state.candidate_job_match.role_specific_risk_areas)

        return "\n".join(part for part in query_parts if part.strip())

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
            candidate_profile=state.candidate_profile,
            job_analysis=state.job_analysis,
            candidate_job_match=state.candidate_job_match,
            company_sources=state.company_sources,
            interview_intel=state.interview_intel,
            interview_planning_skill=self.interview_planning_skill,
            knowledge_context=state.planning_knowledge_context,
        )
        interview_plan = await agent.run()
        return replace(state, interview_plan=interview_plan)

    async def run_live_turn(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def evaluate_session(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def generate_report(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    def build_preparation_graph(self):
        graph = StateGraph(InterviewGraphState)

        graph.add_node("ingest_documents", self.ingest_documents)
        graph.add_node("index_knowledge_base", self.index_knowledge_base)
        graph.add_node("extract_resume_profile", self.extract_resume_profile)
        graph.add_node("profile_candidate", self.profile_candidate)
        graph.add_node("analyze_jd", self.analyze_jd)
        graph.add_node("match_candidate_to_job", self.match_candidate_to_job)
        graph.add_node("research_company", self.research_company)
        graph.add_node("collect_interview_intel", self.collect_interview_intel)
        graph.add_node("retrieve_planning_context", self.retrieve_planning_context)
        graph.add_node("plan_interview", self.plan_interview)

        graph.add_edge(START, "ingest_documents")
        graph.add_edge("ingest_documents", "index_knowledge_base")
        graph.add_edge("index_knowledge_base", "extract_resume_profile")
        graph.add_edge("extract_resume_profile", "profile_candidate")
        graph.add_edge("profile_candidate", "analyze_jd")
        graph.add_edge("analyze_jd", "match_candidate_to_job")
        graph.add_edge("match_candidate_to_job", "research_company")
        graph.add_edge("research_company", "collect_interview_intel")
        graph.add_edge("collect_interview_intel", "retrieve_planning_context")
        graph.add_edge("retrieve_planning_context", "plan_interview")
        graph.add_edge("plan_interview", END)

        return graph.compile()

    def build_live_interview_graph(self):
        graph = StateGraph(InterviewGraphState)

        graph.add_node("run_live_turn", self.run_live_turn)
        graph.add_node("evaluate_session", self.evaluate_session)
        graph.add_node("generate_report", self.generate_report)

        graph.add_edge(START, "run_live_turn")
        graph.add_edge("run_live_turn", "evaluate_session")
        graph.add_edge("evaluate_session", "generate_report")
        graph.add_edge("generate_report", END)

        return graph.compile()
