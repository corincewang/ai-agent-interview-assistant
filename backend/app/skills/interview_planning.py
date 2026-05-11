from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.domain.models import (
    CandidateJobMatch,
    CandidateProfile,
    InterviewPlan,
    JobAnalysis,
    KnowledgeRetrievalResult,
    ResearchFinding,
)
from app.utils.dataclass_mapping import coerce_dataclass


class LLMInterviewPlanningSkill:
    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You create structured technical interview plans. "
                    "Use the candidate profile, job analysis, candidate-job match, company context, "
                    "interview intel, and retrieved knowledge-base context to generate focused "
                    "questions and follow-up strategies. Every question should test a concrete "
                    "signal, risk area, role requirement, or knowledge-base preparation topic. "
                    "Prefer questions grounded in the candidate's resume, JD, or retrieved "
                    "knowledge context. If retrieved knowledge context is provided, at least two "
                    "questions must explicitly target topics from it. Do not invent knowledge-base "
                    "facts that are not present. Do not describe the candidate as lacking or having "
                    "limited experience in a topic when the retrieved context includes concrete "
                    "project notes about that topic.",
                ),
                (
                    "human",
                    "Session ID: {session_id}\n\n"
                    "Candidate profile:\n{candidate_profile}\n\n"
                    "Job analysis:\n{job_analysis}\n\n"
                    "Candidate-job match:\n{candidate_job_match}\n\n"
                    "Company sources:\n{company_sources}\n\n"
                    "Interview intel:\n{interview_intel}\n\n"
                    "Retrieved knowledge-base context:\n{formatted_knowledge_context}",
                ),
            ]
        )

    async def create_interview_plan(
        self,
        session_id: UUID,
        candidate_profile: CandidateProfile,
        job_analysis: JobAnalysis,
        candidate_job_match: CandidateJobMatch,
        company_sources: list[ResearchFinding],
        interview_intel: list[ResearchFinding],
        knowledge_context: KnowledgeRetrievalResult | None = None,
    ) -> InterviewPlan:
        structured_llm = self.llm.with_structured_output(InterviewPlan)
        chain = self.prompt | structured_llm
        extracted = await chain.ainvoke(
            {
                "session_id": str(session_id),
                "candidate_profile": candidate_profile,
                "job_analysis": job_analysis,
                "candidate_job_match": candidate_job_match,
                "company_sources": company_sources,
                "interview_intel": interview_intel,
                "formatted_knowledge_context": _format_knowledge_context(knowledge_context),
            }
        )
        return coerce_dataclass(InterviewPlan, extracted)


def _format_knowledge_context(
    knowledge_context: KnowledgeRetrievalResult | None,
) -> str:
    if knowledge_context is None or not knowledge_context.chunks:
        return "No retrieved knowledge-base context."

    lines = [f"Retrieval query: {knowledge_context.query}"]
    for chunk in knowledge_context.chunks:
        preview = " ".join(chunk.chunk.text.split())[:900]
        lines.append(
            "\n".join(
                [
                    f"- Rank {chunk.rank}, score {chunk.score:.4f}",
                    f"  Chunk index: {chunk.chunk.metadata.get('chunk_index')}",
                    f"  Excerpt: {preview}",
                ]
            )
        )

    if knowledge_context.warnings:
        lines.append(f"Warnings: {knowledge_context.warnings}")

    return "\n\n".join(lines)
