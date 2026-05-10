from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.domain.models import CandidateProfile, ResumeProfile
from app.utils.dataclass_mapping import coerce_dataclass


class LLMCandidateProfilingSkill:
    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You build interview-oriented candidate profiles for technical interviews. "
                    "Use only the structured resume profile provided by the system. "
                    "Separate proven strengths from risk areas and follow-up targets.",
                ),
                (
                    "human",
                    "User ID: {user_id}\n"
                    "Session ID: {session_id}\n\n"
                    "Structured resume profile:\n{resume_profile}",
                ),
            ]
        )

    async def build_candidate_profile(
        self,
        user_id: UUID,
        session_id: UUID,
        resume_profile: ResumeProfile,
    ) -> CandidateProfile:
        structured_llm = self.llm.with_structured_output(CandidateProfile)
        chain = self.prompt | structured_llm
        extracted = await chain.ainvoke(
            {
                "user_id": str(user_id),
                "session_id": str(session_id),
                "resume_profile": resume_profile,
            }
        )
        return coerce_dataclass(CandidateProfile, extracted)
