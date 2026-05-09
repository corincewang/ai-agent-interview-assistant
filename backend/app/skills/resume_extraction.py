from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.domain.models import (
    EducationItem,
    LanguageProficiency,
    ParsedDocument,
    ResumeProfile,
    SkillInventory,
    WorkExperience,
)


class LLMResumeExtractionSkill:
    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You extract structured resume facts for a technical interview assistant. "
                    "Return only facts supported by the resume text. Do not infer missing details.",
                ),
                (
                    "human",
                    "User ID: {user_id}\n\nResume text:\n{resume_text}",
                ),
            ]
        )

    async def extract_resume_profile(
        self,
        user_id: UUID,
        parsed_resume: ParsedDocument,
    ) -> ResumeProfile:
        structured_llm = self.llm.with_structured_output(ResumeProfile)
        chain = self.prompt | structured_llm
        extracted = await chain.ainvoke(
            {
                "user_id": str(user_id),
                "resume_text": parsed_resume.raw_text,
            }
        )

        return self._attach_extraction_warnings(extracted, parsed_resume)

    def _attach_extraction_warnings(
        self,
        profile: ResumeProfile,
        parsed_resume: ParsedDocument,
    ) -> ResumeProfile:
        warnings = list(profile.extraction_warnings)

        if not parsed_resume.raw_text.strip():
            warnings.append("Resume text is empty after parsing.")

        if self._looks_like_pdf_encoding_noise(parsed_resume.raw_text):
            warnings.append(
                "Resume text may contain PDF font encoding noise; OCR fallback may improve extraction."
            )

        return ResumeProfile(
            user_id=profile.user_id,
            name=profile.name,
            education=profile.education,
            skills=profile.skills,
            languages=profile.languages,
            work_experiences=profile.work_experiences,
            project_experiences=profile.project_experiences,
            portfolio_links=profile.portfolio_links,
            extraction_warnings=warnings,
        )

    def _looks_like_pdf_encoding_noise(self, text: str) -> bool:
        if not text:
            return False

        noisy_chars = sum(1 for char in text if "\u0e00" <= char <= "\u0fff")
        return noisy_chars / max(len(text), 1) > 0.03

