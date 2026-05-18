import json
from collections.abc import Awaitable, Callable
from dataclasses import replace
from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import BaseModel, Field

from app.domain.models import (
    CandidateJobMatch,
    CandidateProfile,
    InterviewMode,
    InterviewPlan,
    InterviewPlanCritique,
    InterviewQuestion,
    InterviewQuestionSourceScope,
    InterviewQuestionType,
    JobAnalysis,
    KnowledgeRetrievalResult,
    MemoryRecord,
    ResearchFinding,
)
from app.prompts.interview_planning import (
    InterviewPlanningPromptConfig,
    InterviewPlanningPromptInputs,
    build_interview_planning_prompt,
    build_interview_plan_summary_prompt,
    build_interview_question_slot_prompt,
    build_project_focus_selection_prompt,
)
from app.utils.dataclass_mapping import coerce_dataclass


QuestionGeneratedCallback = Callable[[InterviewQuestion, int], Awaitable[None]]


class ProjectFocus(BaseModel):
    focus_id: str = Field(description="Stable project focus id such as project_1")
    name: str
    evidence_summary: str
    jd_fit_reason: str


class ProjectFocusSelection(BaseModel):
    focuses: list[ProjectFocus]


class InterviewPlanSummary(BaseModel):
    rubric: dict[str, str]
    candidate_storyline: str
    planned_deep_dives: list[str]


class LLMInterviewPlanningSkill:
    def __init__(
        self,
        llm: BaseChatModel,
        prompt_config: InterviewPlanningPromptConfig | None = None,
        question_generated_callback: QuestionGeneratedCallback | None = None,
    ) -> None:
        self.llm = llm
        self.prompt_config = prompt_config or InterviewPlanningPromptConfig()
        self.prompt = build_interview_planning_prompt()
        self.project_focus_prompt = build_project_focus_selection_prompt()
        self.question_slot_prompt = build_interview_question_slot_prompt()
        self.plan_summary_prompt = build_interview_plan_summary_prompt()
        self.question_generated_callback = question_generated_callback

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
        reusable_question_memories: list[MemoryRecord] | None = None,
        previous_plan_critique: InterviewPlanCritique | None = None,
    ) -> InterviewPlan:
        project_focuses = await self._select_project_focuses(
            target_track=target_track,
            candidate_profile=candidate_profile,
            job_analysis=job_analysis,
            candidate_job_match=candidate_job_match,
            knowledge_context=knowledge_context,
        )
        question_blueprint = self._build_question_blueprint(project_focuses)
        prompt_inputs = self._build_prompt_inputs(
            session_id=session_id,
            target_track=target_track,
            candidate_profile=candidate_profile,
            job_analysis=job_analysis,
            candidate_job_match=candidate_job_match,
            company_sources=company_sources,
            interview_intel=interview_intel,
            knowledge_context=knowledge_context,
            reusable_question_memories=reusable_question_memories or [],
            question_blueprint=question_blueprint,
            previous_plan_critique=previous_plan_critique,
        )

        questions: list[InterviewQuestion] = []
        for slot in question_blueprint:
            question = await self._generate_question_for_slot(
                slot=slot,
                generated_questions=questions,
                selected_project_focuses=project_focuses,
                prompt_inputs=prompt_inputs,
            )
            questions.append(question)
            if self.question_generated_callback is not None:
                await self.question_generated_callback(question, len(questions))

        summary = await self._generate_plan_summary(
            target_track=target_track,
            candidate_profile=candidate_profile,
            job_analysis=job_analysis,
            candidate_job_match=candidate_job_match,
            project_focuses=project_focuses,
            questions=questions,
        )

        plan = InterviewPlan(
            session_id=session_id,
            mode=InterviewMode.GENERAL_SWE,
            questions=questions,
            rubric=summary.rubric,
            candidate_storyline=summary.candidate_storyline,
            planned_deep_dives=summary.planned_deep_dives,
            target_track=target_track,
        )
        self._validate_plan_contract(plan)
        return plan

    async def _select_project_focuses(
        self,
        target_track: str,
        candidate_profile: CandidateProfile,
        job_analysis: JobAnalysis,
        candidate_job_match: CandidateJobMatch,
        knowledge_context: KnowledgeRetrievalResult | None,
    ) -> list[ProjectFocus]:
        structured_llm = self.llm.with_structured_output(ProjectFocusSelection)
        chain = self.project_focus_prompt | structured_llm
        extracted = await chain.ainvoke(
            {
                **self.prompt_config.as_template_variables(),
                "target_track": target_track,
                "candidate_profile": str(candidate_profile),
                "job_analysis": str(job_analysis),
                "candidate_job_match": str(candidate_job_match),
                "formatted_knowledge_context": format_knowledge_context_for_prompt(
                    knowledge_context
                ),
            }
        )
        selection = extracted if isinstance(extracted, ProjectFocusSelection) else ProjectFocusSelection.model_validate(extracted)
        focuses = selection.focuses[: self.prompt_config.selected_project_count]
        return _ensure_project_focus_count(
            focuses=focuses,
            candidate_profile=candidate_profile,
            expected_count=self.prompt_config.selected_project_count,
        )

    def _build_prompt_inputs(
        self,
        session_id: UUID,
        target_track: str,
        candidate_profile: CandidateProfile,
        job_analysis: JobAnalysis,
        candidate_job_match: CandidateJobMatch,
        company_sources: list[ResearchFinding],
        interview_intel: list[ResearchFinding],
        knowledge_context: KnowledgeRetrievalResult | None,
        reusable_question_memories: list[MemoryRecord],
        question_blueprint: list[dict],
        previous_plan_critique: InterviewPlanCritique | None,
    ) -> InterviewPlanningPromptInputs:
        return InterviewPlanningPromptInputs(
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
            formatted_reusable_question_memories=(
                format_reusable_question_memories_for_prompt(
                    reusable_question_memories
                )
            ),
            question_blueprint=json.dumps(question_blueprint, ensure_ascii=False),
            previous_plan_critique=format_previous_plan_critique_for_prompt(
                previous_plan_critique
            ),
            validation_feedback="No validation feedback.",
            extra_variables=self.prompt_config.as_template_variables(),
        )

    def _build_question_blueprint(self, project_focuses: list[ProjectFocus]) -> list[dict]:
        blueprint: list[dict] = []

        for project_focus in project_focuses:
            for question_index in range(self.prompt_config.project_questions_per_focus):
                source_scope = (
                    InterviewQuestionSourceScope.RESUME_WRITTEN
                    if question_index == 0
                    else InterviewQuestionSourceScope.RESUME_UNWRITTEN
                )
                blueprint.append(
                    {
                        "question_type": InterviewQuestionType.PROJECT_DEEP_DIVE.value,
                        "allowed_source_scopes": [source_scope.value],
                        "project_focus_id": project_focus.focus_id,
                        "project_focus_name": project_focus.name,
                        "project_question_role": (
                            "resume_bulletpoint_probe"
                            if question_index == 0
                            else "adjacent_project_deep_dive"
                        ),
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

    async def _generate_question_for_slot(
        self,
        slot: dict,
        generated_questions: list[InterviewQuestion],
        selected_project_focuses: list[ProjectFocus],
        prompt_inputs: InterviewPlanningPromptInputs,
    ) -> InterviewQuestion:
        structured_llm = self.llm.with_structured_output(InterviewQuestion)
        chain = self.question_slot_prompt | structured_llm
        last_error_message = "unknown question validation error"

        for _ in range(self.prompt_config.max_generation_attempts):
            extracted = await chain.ainvoke(
                {
                    **prompt_inputs.as_template_variables(),
                    "question_slot": json.dumps(slot, ensure_ascii=False),
                    "selected_project_focuses": _format_project_focuses(
                        selected_project_focuses
                    ),
                    "generated_questions": format_generated_questions_for_prompt(
                        generated_questions
                    ),
                }
            )
            question = coerce_dataclass(InterviewQuestion, extracted)
            question = self._apply_slot(question=question, slot=slot)
            try:
                self._validate_question_slot(question=question, slot=slot)
                return question
            except ValueError as error:
                last_error_message = str(error)

        raise ValueError(f"InterviewQuestion validation failed: {last_error_message}")

    async def _generate_plan_summary(
        self,
        target_track: str,
        candidate_profile: CandidateProfile,
        job_analysis: JobAnalysis,
        candidate_job_match: CandidateJobMatch,
        project_focuses: list[ProjectFocus],
        questions: list[InterviewQuestion],
    ) -> InterviewPlanSummary:
        structured_llm = self.llm.with_structured_output(InterviewPlanSummary)
        chain = self.plan_summary_prompt | structured_llm
        extracted = await chain.ainvoke(
            {
                **self.prompt_config.as_template_variables(),
                "target_track": target_track,
                "candidate_profile": str(candidate_profile),
                "job_analysis": str(job_analysis),
                "candidate_job_match": str(candidate_job_match),
                "selected_project_focuses": _format_project_focuses(project_focuses),
                "generated_questions": format_generated_questions_for_prompt(questions),
            }
        )
        if isinstance(extracted, InterviewPlanSummary):
            return extracted
        return InterviewPlanSummary.model_validate(extracted)

    def _apply_slot(self, question: InterviewQuestion, slot: dict) -> InterviewQuestion:
        slot_type = InterviewQuestionType(slot["question_type"])
        allowed_scope_values = slot["allowed_source_scopes"]
        allowed_scopes = [InterviewQuestionSourceScope(v) for v in allowed_scope_values]
        source_scope = question.source_scope
        if source_scope not in allowed_scopes:
            source_scope = allowed_scopes[0]
        return replace(question, question_type=slot_type, source_scope=source_scope)

    def _validate_question_slot(self, question: InterviewQuestion, slot: dict) -> None:
        if question.question_type != InterviewQuestionType(slot["question_type"]):
            raise ValueError("question_type does not match slot")
        allowed_scopes = [
            InterviewQuestionSourceScope(value)
            for value in slot["allowed_source_scopes"]
        ]
        if question.source_scope not in allowed_scopes:
            raise ValueError("source_scope does not match slot")
        if question.why_asked is None or not question.why_asked.strip():
            raise ValueError("why_asked is required")
        if not question.expected_signals:
            raise ValueError("expected_signals is required")
        if not question.follow_up_strategy:
            raise ValueError("follow_up_strategy is required")

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


def format_reusable_question_memories_for_prompt(
    memories: list[MemoryRecord],
) -> str:
    if not memories:
        return "No reusable long-term question memories."

    lines: list[str] = []
    for index, memory in enumerate(memories[:8], start=1):
        prompt = str(memory.content.get("prompt", "")).strip()
        if not prompt:
            continue

        metadata = memory.metadata
        lines.append(
            "\n".join(
                [
                    f"[Memory {index}]",
                    f"quality_score={memory.quality_score}",
                    f"question_type={metadata.get('question_type')}",
                    f"source_scope={metadata.get('source_scope')}",
                    f"topic={memory.content.get('topic')}",
                    f"prompt={prompt}",
                ]
            )
        )

    if not lines:
        return "No reusable long-term question memories with prompt content."

    return "\n\n".join(lines)


def format_generated_questions_for_prompt(
    questions: list[InterviewQuestion],
) -> str:
    if not questions:
        return "No questions have been generated yet."

    lines: list[str] = []
    for index, question in enumerate(questions, start=1):
        lines.append(
            "\n".join(
                [
                    f"[Q{index}]",
                    f"question_type={question.question_type}",
                    f"source_scope={question.source_scope}",
                    f"topic={question.topic}",
                    f"prompt={question.prompt}",
                ]
            )
        )
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


def _ensure_project_focus_count(
    focuses: list[ProjectFocus],
    candidate_profile: CandidateProfile,
    expected_count: int,
) -> list[ProjectFocus]:
    normalized = focuses[:expected_count]
    used_names = {focus.name.strip().lower() for focus in normalized}

    for highlight in candidate_profile.project_highlights:
        if len(normalized) >= expected_count:
            break
        name = highlight.strip()[:80] or f"Project {len(normalized) + 1}"
        if name.lower() in used_names:
            continue
        normalized.append(
            ProjectFocus(
                focus_id=f"project_{len(normalized) + 1}",
                name=name,
                evidence_summary=highlight,
                jd_fit_reason="Fallback focus from candidate project highlights.",
            )
        )
        used_names.add(name.lower())

    while len(normalized) < expected_count:
        normalized.append(
            ProjectFocus(
                focus_id=f"project_{len(normalized) + 1}",
                name=f"Candidate project focus {len(normalized) + 1}",
                evidence_summary="Not enough explicit project highlights were available.",
                jd_fit_reason="Use candidate/JD fit evidence to create a careful adjacent project deep dive.",
            )
        )

    return [
        focus.model_copy(update={"focus_id": f"project_{index}"})
        for index, focus in enumerate(normalized, start=1)
    ]


def _format_project_focuses(project_focuses: list[ProjectFocus]) -> str:
    return "\n\n".join(
        "\n".join(
            [
                f"[{focus.focus_id}] {focus.name}",
                f"evidence_summary={focus.evidence_summary}",
                f"jd_fit_reason={focus.jd_fit_reason}",
            ]
        )
        for focus in project_focuses
    )
