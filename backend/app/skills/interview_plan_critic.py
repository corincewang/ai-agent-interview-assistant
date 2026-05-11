from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel

from app.domain.models import (
    CandidateJobMatch,
    CandidateProfile,
    InterviewPlan,
    InterviewPlanCritique,
    JobAnalysis,
    KnowledgeRetrievalResult,
)
from app.prompts.interview_plan_critic import (
    InterviewPlanCriticPromptConfig,
    InterviewPlanCriticPromptInputs,
    build_interview_plan_critic_prompt,
)
from app.skills.interview_planning import format_knowledge_context_for_prompt
from app.utils.dataclass_mapping import coerce_dataclass


class LLMInterviewPlanCriticSkill:
    def __init__(
        self,
        llm: BaseChatModel,
        prompt_config: InterviewPlanCriticPromptConfig | None = None,
    ) -> None:
        self.llm = llm
        self.prompt_config = prompt_config or InterviewPlanCriticPromptConfig()
        self.prompt = build_interview_plan_critic_prompt()

    async def critique_interview_plan(
        self,
        session_id: UUID,
        interview_plan: InterviewPlan,
        candidate_profile: CandidateProfile,
        job_analysis: JobAnalysis,
        candidate_job_match: CandidateJobMatch,
        knowledge_context: KnowledgeRetrievalResult | None = None,
    ) -> InterviewPlanCritique:
        structured_llm = self.llm.with_structured_output(InterviewPlanCritique)
        chain = self.prompt | structured_llm
        prompt_inputs = InterviewPlanCriticPromptInputs(
            session_id=str(session_id),
            interview_plan=str(interview_plan),
            candidate_profile=str(candidate_profile),
            job_analysis=str(job_analysis),
            candidate_job_match=str(candidate_job_match),
            formatted_knowledge_context=format_knowledge_context_for_prompt(knowledge_context),
            extra_variables=self.prompt_config.as_template_variables(),
        )
        extracted = await chain.ainvoke(prompt_inputs.as_template_variables())
        return coerce_dataclass(InterviewPlanCritique, extracted)
