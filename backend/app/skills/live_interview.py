from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool, tool
from langgraph.prebuilt import create_react_agent

from app.domain.models import (
    InterviewPlan,
    InterviewQuestion,
    InterviewQuestionType,
    InterviewTurn,
)


class LiveInterviewDecision(BaseModel):
    action: str = Field(
        description="One of: use_planned_question, ask_follow_up, move_on."
    )
    question_id: str | None = None
    prompt: str | None = None
    topic: str | None = None
    difficulty: str = "medium"
    expected_signals: list[str] = Field(default_factory=list)
    follow_up_strategy: list[str] = Field(default_factory=list)


class LLMLiveInterviewSkill:
    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm

    async def select_next_question(
        self,
        session_id: UUID,
        plan: InterviewPlan,
        transcript: list[InterviewTurn],
    ) -> InterviewQuestion:
        decision = await self._run_live_react_agent(
            task=(
                "Select the next interview question. Prefer an unanswered planned question. "
                "Only create a new question if every planned question has already been answered."
            ),
            session_id=session_id,
            plan=plan,
            transcript=transcript,
        )
        planned_question = self._question_from_decision(plan, decision)
        if planned_question is not None:
            return planned_question

        unanswered = self._first_unanswered_question(plan, transcript)
        if unanswered is not None:
            return unanswered

        return self._build_generated_question(decision, fallback_topic="general")

    async def decide_follow_up(
        self,
        session_id: UUID,
        current_question: InterviewQuestion,
        candidate_answer: str,
        transcript: list[InterviewTurn],
    ) -> InterviewQuestion | None:
        if len(candidate_answer.strip()) < 80:
            return self._build_short_answer_follow_up(current_question)

        decision = await self._run_live_react_agent(
            task=(
                "Decide whether to ask a follow-up question. Ask a follow-up only when the "
                "candidate answer is incomplete, shallow, inconsistent, or worth deeper probing. "
                "Return action=move_on when the interviewer should move on."
            ),
            session_id=session_id,
            plan=None,
            transcript=transcript,
            current_question=current_question,
            candidate_answer=candidate_answer,
        )
        if decision.action == "move_on":
            return None
        if not decision.prompt:
            return None
        return self._build_generated_question(decision, fallback_topic=current_question.topic)

    async def _run_live_react_agent(
        self,
        task: str,
        session_id: UUID,
        plan: InterviewPlan | None,
        transcript: list[InterviewTurn],
        current_question: InterviewQuestion | None = None,
        candidate_answer: str | None = None,
    ) -> LiveInterviewDecision:
        agent = create_react_agent(
            model=self.llm,
            tools=self._build_live_tools(plan=plan, transcript=transcript),
            prompt=(
                "You are a technical mock interviewer. Use tools before deciding when they help. "
                "Keep the interview grounded in the plan and transcript. "
                "Do not repeat questions that already have candidate answers. "
                "Return a structured decision only."
            ),
            response_format=LiveInterviewDecision,
            name="live_interview_react_agent",
        )
        response = await agent.ainvoke(
            {
                "messages": [
                    HumanMessage(
                        content=(
                            f"Session ID: {session_id}\n"
                            f"Task: {task}\n"
                            f"Current question: {current_question}\n"
                            f"Candidate answer: {candidate_answer}\n"
                        )
                    )
                ]
            }
        )
        structured_response = response.get("structured_response")
        if structured_response is None:
            return LiveInterviewDecision(action="move_on")
        return structured_response

    def _build_live_tools(
        self,
        plan: InterviewPlan | None,
        transcript: list[InterviewTurn],
    ) -> list[BaseTool]:
        @tool
        async def list_unanswered_planned_questions() -> list[dict]:
            """List planned interview questions that do not have candidate answers yet."""
            if plan is None:
                return []

            answered_question_ids = self._answered_question_ids(transcript)
            questions: list[dict] = []
            for question in plan.questions:
                if str(question.id) in answered_question_ids:
                    continue
                questions.append(
                    {
                        "id": str(question.id),
                        "prompt": question.prompt,
                        "topic": question.topic,
                        "difficulty": question.difficulty,
                        "question_type": (
                            question.question_type.value
                            if question.question_type is not None
                            else None
                        ),
                    }
                )
            return questions

        @tool
        async def summarize_transcript() -> str:
            """Return a compact transcript summary for recent interview turns."""
            lines: list[str] = []
            for turn in transcript[-12:]:
                lines.append(f"{turn.role.value}: {turn.content}")
            return "\n".join(lines)

        return [list_unanswered_planned_questions, summarize_transcript]

    def _first_unanswered_question(
        self,
        plan: InterviewPlan,
        transcript: list[InterviewTurn],
    ) -> InterviewQuestion | None:
        answered_question_ids = self._answered_question_ids(transcript)

        for question in plan.questions:
            if str(question.id) not in answered_question_ids:
                return question

        return None

    def _answered_question_ids(self, transcript: list[InterviewTurn]) -> set[str]:
        answered_question_ids: set[str] = set()
        for turn in transcript:
            question_id = turn.metadata.get("question_id")
            if question_id is not None:
                answered_question_ids.add(str(question_id))
        return answered_question_ids

    def _question_from_decision(
        self,
        plan: InterviewPlan,
        decision: LiveInterviewDecision,
    ) -> InterviewQuestion | None:
        if decision.action != "use_planned_question":
            return None
        if decision.question_id is None:
            return None

        for question in plan.questions:
            if str(question.id) == decision.question_id:
                return question
        return None

    def _build_generated_question(
        self,
        decision: LiveInterviewDecision,
        fallback_topic: str,
    ) -> InterviewQuestion:
        difficulty = decision.difficulty
        if difficulty not in {"easy", "medium", "hard"}:
            difficulty = "medium"

        return InterviewQuestion(
            id=uuid4(),
            prompt=decision.prompt or "Can you expand on the implementation details and tradeoffs?",
            topic=decision.topic or fallback_topic,
            difficulty=difficulty,
            expected_signals=decision.expected_signals,
            follow_up_strategy=decision.follow_up_strategy,
            question_type=InterviewQuestionType.TECH_DEEP_DIVE,
        )

    def _build_short_answer_follow_up(
        self,
        current_question: InterviewQuestion,
    ) -> InterviewQuestion:
        return InterviewQuestion(
            id=uuid4(),
            prompt="Can you go deeper and explain the tradeoffs, implementation details, and edge cases?",
            topic=current_question.topic,
            difficulty=current_question.difficulty,
            expected_signals=current_question.expected_signals,
            follow_up_strategy=current_question.follow_up_strategy,
            question_type=current_question.question_type,
            why_asked=current_question.why_asked,
            evidence_chunk_ids=current_question.evidence_chunk_ids,
            source_scope=current_question.source_scope,
        )
