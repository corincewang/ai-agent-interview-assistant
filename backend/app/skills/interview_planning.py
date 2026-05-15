import json
from dataclasses import replace
from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel

from app.domain.models import (
    CandidateJobMatch,
    CandidateProfile,
    InterviewPlan,
    InterviewPlanCritique,
    InterviewQuestion,
    InterviewQuestionSourceScope,
    InterviewQuestionType,
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
        target_track: str,
        candidate_profile: CandidateProfile,
        job_analysis: JobAnalysis,
        candidate_job_match: CandidateJobMatch,
        company_sources: list[ResearchFinding],
        interview_intel: list[ResearchFinding],
        knowledge_context: KnowledgeRetrievalResult | None = None,
        previous_plan_critique: InterviewPlanCritique | None = None,
    ) -> InterviewPlan:
        structured_llm = self.llm.with_structured_output(InterviewPlan)
        chain = self.prompt | structured_llm
        validation_feedback = "No validation feedback."
        last_error_message = "unknown validation error"
        question_blueprint = self._build_question_blueprint()

        for attempt in range(1, self.prompt_config.max_generation_attempts + 1):
            prompt_inputs = InterviewPlanningPromptInputs(
                session_id=str(session_id),
                target_track=target_track,
                candidate_profile=str(candidate_profile),
                job_analysis=str(job_analysis),
                candidate_job_match=str(candidate_job_match),
                company_sources=str(company_sources),
                interview_intel=str(interview_intel),
                formatted_knowledge_context=format_knowledge_context_for_prompt(
                    knowledge_context
                ),
                question_blueprint=json.dumps(question_blueprint, ensure_ascii=False),
                previous_plan_critique=format_previous_plan_critique_for_prompt(
                    previous_plan_critique
                ),
                validation_feedback=validation_feedback,
                extra_variables=self.prompt_config.as_template_variables(),
            )
            extracted = await chain.ainvoke(prompt_inputs.as_template_variables())
            plan = coerce_dataclass(InterviewPlan, extracted)
            finalized_plan = InterviewPlan(
                session_id=plan.session_id,
                mode=plan.mode,
                questions=self._apply_blueprint(
                    questions=plan.questions,
                    question_blueprint=question_blueprint,
                ),
                rubric=plan.rubric,
                candidate_storyline=plan.candidate_storyline,
                planned_deep_dives=plan.planned_deep_dives,
                target_track=target_track,
                revised=plan.revised,
                revision_attempts_used=plan.revision_attempts_used,
            )
            try:
                self._validate_plan_contract(finalized_plan)
                return finalized_plan
            except ValueError as error:
                last_error_message = str(error)
                validation_feedback = (
                    "Previous attempt failed validation. "
                    f"Attempt={attempt}. Error={last_error_message}. "
                    "Regenerate the full plan and satisfy all strict counts and source_scope constraints."
                )

        raise ValueError(
            "InterviewPlan validation failed after retries. "
            f"Last error: {last_error_message}"
        )

    def _build_question_blueprint(self) -> list[dict]:
        blueprint: list[dict] = []

        for _ in range(self.prompt_config.project_deep_dive_count):
            blueprint.append(
                {
                    "question_type": InterviewQuestionType.PROJECT_DEEP_DIVE.value,
                    "allowed_source_scopes": [
                        InterviewQuestionSourceScope.RESUME_WRITTEN.value,
                        InterviewQuestionSourceScope.RESUME_UNWRITTEN.value,
                    ],
                }
            )
        for _ in range(self.prompt_config.tech_deep_dive_count):
            blueprint.append(
                {
                    "question_type": InterviewQuestionType.TECH_DEEP_DIVE.value,
                    "allowed_source_scopes": [
                        InterviewQuestionSourceScope.TECH_STACK.value,
                    ],
                }
            )
        for _ in range(self.prompt_config.scenario_count):
            blueprint.append(
                {
                    "question_type": InterviewQuestionType.SCENARIO.value,
                    "allowed_source_scopes": [
                        InterviewQuestionSourceScope.JD_SCENARIO.value,
                        InterviewQuestionSourceScope.TECH_STACK.value,
                        InterviewQuestionSourceScope.RESUME_WRITTEN.value,
                        InterviewQuestionSourceScope.RESUME_UNWRITTEN.value,
                        InterviewQuestionSourceScope.INTERVIEW_INTEL_WEB.value,
                    ],
                }
            )
        return blueprint

    def _apply_blueprint(
        self,
        questions: list[InterviewQuestion],
        question_blueprint: list[dict],
    ) -> list[InterviewQuestion]:
        aligned: list[InterviewQuestion] = []
        for index, blueprint_slot in enumerate(question_blueprint):
            if index >= len(questions):
                break
            question = questions[index]
            slot_type = InterviewQuestionType(blueprint_slot["question_type"])
            allowed_scope_values = blueprint_slot["allowed_source_scopes"]
            allowed_scopes = [InterviewQuestionSourceScope(v) for v in allowed_scope_values]
            source_scope = question.source_scope
            if source_scope not in allowed_scopes:
                source_scope = allowed_scopes[0]
            aligned.append(
                replace(
                    question,
                    question_type=slot_type,
                    source_scope=source_scope,
                )
            )
        return aligned

    def _validate_plan_contract(self, plan: InterviewPlan) -> None:
        expected_count = self.prompt_config.target_question_count
        if len(plan.questions) != expected_count:
            raise ValueError(
                f"InterviewPlan question count mismatch: expected {expected_count}, got {len(plan.questions)}."
            )

        project_count = 0
        tech_count = 0
        scenario_count = 0

        for index, question in enumerate(plan.questions):
            if question.question_type is None:
                raise ValueError(
                    f"InterviewPlan question at index {index} is missing question_type."
                )
            if question.source_scope is None:
                raise ValueError(
                    f"InterviewPlan question at index {index} is missing source_scope."
                )
            if question.why_asked is None or not question.why_asked.strip():
                raise ValueError(
                    f"InterviewPlan question at index {index} is missing why_asked."
                )

            if question.question_type == InterviewQuestionType.PROJECT_DEEP_DIVE:
                if question.source_scope not in (
                    InterviewQuestionSourceScope.RESUME_WRITTEN,
                    InterviewQuestionSourceScope.RESUME_UNWRITTEN,
                ):
                    raise ValueError(
                        "InterviewPlan project_deep_dive source_scope mismatch: "
                        f"expected resume_written/resume_unwritten, got {question.source_scope}."
                    )
                project_count += 1
            elif question.question_type == InterviewQuestionType.TECH_DEEP_DIVE:
                if question.source_scope != InterviewQuestionSourceScope.TECH_STACK:
                    raise ValueError(
                        "InterviewPlan tech_deep_dive source_scope mismatch: "
                        f"expected tech_stack, got {question.source_scope}."
                    )
                tech_count += 1
            elif question.question_type == InterviewQuestionType.SCENARIO:
                if question.source_scope not in (
                    InterviewQuestionSourceScope.JD_SCENARIO,
                    InterviewQuestionSourceScope.TECH_STACK,
                    InterviewQuestionSourceScope.RESUME_WRITTEN,
                    InterviewQuestionSourceScope.RESUME_UNWRITTEN,
                    InterviewQuestionSourceScope.INTERVIEW_INTEL_WEB,
                ):
                    raise ValueError(
                        "InterviewPlan scenario source_scope mismatch: "
                        "expected one of "
                        "jd_scenario/tech_stack/resume_written/resume_unwritten/interview_intel_web, "
                        f"got {question.source_scope}."
                    )
                scenario_count += 1

        expected_project_count = self.prompt_config.project_deep_dive_count
        if project_count != expected_project_count:
            raise ValueError(
                "InterviewPlan project_deep_dive count mismatch: "
                f"expected {expected_project_count}, got {project_count}."
            )

        expected_tech_count = self.prompt_config.tech_deep_dive_count
        if tech_count != expected_tech_count:
            raise ValueError(
                "InterviewPlan tech_deep_dive count mismatch: "
                f"expected {expected_tech_count}, got {tech_count}."
            )

        expected_scenario_count = self.prompt_config.scenario_count
        if scenario_count != expected_scenario_count:
            raise ValueError(
                "InterviewPlan scenario count mismatch: "
                f"expected {expected_scenario_count}, got {scenario_count}."
            )


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


def format_previous_plan_critique_for_prompt(
    previous_plan_critique: InterviewPlanCritique | None,
) -> str:
    if previous_plan_critique is None:
        return "No previous plan critique."

    lines: list[str] = []
    lines.append(f"overall_score={previous_plan_critique.overall_score:.3f}")
    lines.append(f"quality_gate_passed={previous_plan_critique.quality_gate_passed}")

    if previous_plan_critique.revision_recommendations:
        lines.append("revision_recommendations:")
        for recommendation in previous_plan_critique.revision_recommendations:
            lines.append(f"- {recommendation}")

    if previous_plan_critique.web_intel_risk_notes:
        lines.append("web_intel_risk_notes:")
        for note in previous_plan_critique.web_intel_risk_notes:
            lines.append(f"- {note}")

    low_score_question_count = 0
    for question_critique in previous_plan_critique.question_critiques:
        if question_critique.overall_score < 0.7:
            low_score_question_count += 1

    lines.append(f"low_score_question_count(<0.7)={low_score_question_count}")
    return "\n".join(lines)
