from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.domain.models import AnswerEvaluation, InterviewQuestion


class LLMAnswerEvaluationSkill:
    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You evaluate technical interview answers. "
                    "Score the answer against correctness, depth, communication, tradeoff awareness, "
                    "and role relevance. Be specific and actionable.",
                ),
                (
                    "human",
                    "Session ID: {session_id}\n\n"
                    "Question:\n{question}\n\n"
                    "Candidate answer:\n{candidate_answer}",
                ),
            ]
        )

    async def evaluate_answer(
        self,
        session_id: UUID,
        question: InterviewQuestion,
        candidate_answer: str,
    ) -> AnswerEvaluation:
        structured_llm = self.llm.with_structured_output(AnswerEvaluation)
        chain = self.prompt | structured_llm
        return await chain.ainvoke(
            {
                "session_id": str(session_id),
                "question": question,
                "candidate_answer": candidate_answer,
            }
        )

