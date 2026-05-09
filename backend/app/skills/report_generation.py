from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.domain.models import AnswerEvaluation, InterviewTurn


class LLMReportGenerationSkill:
    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You generate concise technical mock interview feedback reports. "
                    "Summarize performance, identify recurring weaknesses, highlight strengths, "
                    "and propose a practical next practice plan.",
                ),
                (
                    "human",
                    "Session ID: {session_id}\n\n"
                    "Transcript:\n{transcript}\n\n"
                    "Answer evaluations:\n{evaluations}",
                ),
            ]
        )

    async def generate_final_report(
        self,
        session_id: UUID,
        transcript: list[InterviewTurn],
        evaluations: list[AnswerEvaluation],
    ) -> str:
        chain = self.prompt | self.llm
        response = await chain.ainvoke(
            {
                "session_id": str(session_id),
                "transcript": transcript,
                "evaluations": evaluations,
            }
        )
        return response.content

