from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.domain.models import InterviewPlan, InterviewQuestion, InterviewTurn
from app.utils.dataclass_mapping import coerce_dataclass


class LLMLiveInterviewSkill:
    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm
        self.next_question_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are selecting the next question for a technical mock interview. "
                    "Use the interview plan and transcript. Prefer planned questions that have not been answered yet.",
                ),
                (
                    "human",
                    "Session ID: {session_id}\n\n"
                    "Interview plan:\n{plan}\n\n"
                    "Transcript:\n{transcript}",
                ),
            ]
        )
        self.follow_up_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You decide whether to ask a technical follow-up question. "
                    "Ask a follow-up only when the answer is incomplete, shallow, inconsistent, or worth deeper probing. "
                    "Return null when the interviewer should move on.",
                ),
                (
                    "human",
                    "Session ID: {session_id}\n\n"
                    "Current question:\n{current_question}\n\n"
                    "Candidate answer:\n{candidate_answer}\n\n"
                    "Transcript:\n{transcript}",
                ),
            ]
        )

    async def select_next_question(
        self,
        session_id: UUID,
        plan: InterviewPlan,
        transcript: list[InterviewTurn],
    ) -> InterviewQuestion:
        unanswered = self._first_unanswered_question(plan, transcript)
        if unanswered is not None:
            return unanswered

        structured_llm = self.llm.with_structured_output(InterviewQuestion)
        chain = self.next_question_prompt | structured_llm
        return await chain.ainvoke(
            {
                "session_id": str(session_id),
                "plan": plan,
                "transcript": transcript,
            }
        )

    async def decide_follow_up(
        self,
        session_id: UUID,
        current_question: InterviewQuestion,
        candidate_answer: str,
        transcript: list[InterviewTurn],
    ) -> InterviewQuestion | None:
        if len(candidate_answer.strip()) < 80:
            return self._build_short_answer_follow_up(current_question)

        structured_llm = self.llm.with_structured_output(InterviewQuestion)
        chain = self.follow_up_prompt | structured_llm
        extracted = await chain.ainvoke(
            {
                "session_id": str(session_id),
                "current_question": current_question,
                "candidate_answer": candidate_answer,
                "transcript": transcript,
            }
        )
        return coerce_dataclass(InterviewQuestion, extracted)

    def _first_unanswered_question(
        self,
        plan: InterviewPlan,
        transcript: list[InterviewTurn],
    ) -> InterviewQuestion | None:
        answered_question_ids = {
            turn.metadata.get("question_id")
            for turn in transcript
            if turn.metadata.get("question_id") is not None
        }

        for question in plan.questions:
            if str(question.id) not in answered_question_ids:
                return question

        return None

    def _build_short_answer_follow_up(
        self,
        current_question: InterviewQuestion,
    ) -> InterviewQuestion:
        return InterviewQuestion(
            id=current_question.id,
            prompt="Can you go deeper and explain the tradeoffs, implementation details, and edge cases?",
            topic=current_question.topic,
            difficulty=current_question.difficulty,
            expected_signals=current_question.expected_signals,
            follow_up_strategy=current_question.follow_up_strategy,
        )
