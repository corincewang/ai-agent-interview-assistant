from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel

from app.domain.models import (
    CandidateJobMatch,
    CandidateProfile,
    InterviewPlan,
    JobAnalysis,
    KnowledgeRetrievalResult,
    ResearchFinding,
)
from app.prompts.interview_planning import (
    InterviewPlanningPromptConfig,
    InterviewPlanningPromptInputs,
    build_interview_planning_prompt,
)
from app.utils.dataclass_mapping import coerce_dataclass


class LLMInterviewPlanningSkill:
    def __init__(
        self,
        llm: BaseChatModel,
        prompt_config: InterviewPlanningPromptConfig | None = None,
    ) -> None:
        self.llm = llm
        self.prompt_config = prompt_config or InterviewPlanningPromptConfig()
        self.prompt = build_interview_planning_prompt()

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
        prompt_inputs = InterviewPlanningPromptInputs(
            session_id=str(session_id),
            candidate_profile=str(candidate_profile),
            job_analysis=str(job_analysis),
            candidate_job_match=str(candidate_job_match),
            company_sources=str(company_sources),
            interview_intel=str(interview_intel),
            formatted_knowledge_context=format_knowledge_context_for_prompt(
                knowledge_context
            ),
            extra_variables=self.prompt_config.as_template_variables(),
        )
        extracted = await chain.ainvoke(prompt_inputs.as_template_variables())
        return coerce_dataclass(InterviewPlan, extracted)


def format_knowledge_context_for_prompt(
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
