from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel

from app.domain.models import (
    CandidateJobMatch,
    CandidateProfile,
    InterviewPlan,
    InterviewPlanCritique,
    InterviewQuestionSourceScope,
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
        critique = coerce_dataclass(InterviewPlanCritique, extracted)
        web_intel_used = False
        for question in interview_plan.questions:
            if question.source_scope == InterviewQuestionSourceScope.INTERVIEW_INTEL_WEB:
                web_intel_used = True
                break

        web_intel_risk_notes = list(critique.web_intel_risk_notes)
        if web_intel_used and len(web_intel_risk_notes) == 0:
            web_intel_risk_notes.append(
                "Plan uses interview_intel_web source. Review whether each related question is grounded in candidate resume/JD evidence and not only web anecdotes."
            )

        return InterviewPlanCritique(
            session_id=critique.session_id,
            overall_score=critique.overall_score,
            quality_gate_passed=critique.quality_gate_passed,
            question_critiques=critique.question_critiques,
            coverage_summary=critique.coverage_summary,
            revision_recommendations=critique.revision_recommendations,
            web_intel_risk_notes=web_intel_risk_notes,
        )
