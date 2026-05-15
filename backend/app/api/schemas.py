from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from app.domain.models import DocumentType, InterviewMode


class CreateInterviewSessionRequest(BaseModel):
    company_name: str = Field(min_length=1)
    role_title: str = Field(min_length=1)
    target_track: str = Field(min_length=1)
    jd_text: str | None = None
    job_description: str | None = None
    mode: InterviewMode = InterviewMode.GENERAL_SWE

    @model_validator(mode="after")
    def _normalize_deprecated_fields(self):
        if not self.jd_text and self.job_description:
            self.jd_text = self.job_description
        if not self.jd_text:
            raise ValueError("jd_text is required")
        return self


class CreateInterviewSessionResponse(BaseModel):
    session_id: UUID
    company_name: str
    role_title: str
    target_track: str


class UploadDocumentResponse(BaseModel):
    session_id: UUID
    document_type: DocumentType
    file_name: str


class BatchUploadDocumentsResponse(BaseModel):
    session_id: UUID
    document_type: DocumentType
    document_count: int
    file_names: list[str]


class PrepareSessionResponse(BaseModel):
    session_id: UUID
    interview_plan: dict
    interview_plan_critique: dict | None = None
    revised: bool
    revision_attempts_used: int


class InterviewPlanResponse(BaseModel):
    session_id: UUID
    interview_plan: dict
    revised: bool
    revision_attempts_used: int


class InterviewSessionDatabaseSummaryResponse(BaseModel):
    session_id: UUID
    company_name: str
    role_title: str
    target_track: str
    status: str
    document_count: int
    parsed_document_count: int
    chunk_count: int
    embedded_chunk_count: int
    plan_count: int
    question_count: int
    critique_count: int
    critique_overall_score: float | None
    critique_quality_gate_passed: bool | None


class SubmitAnswerRequest(BaseModel):
    question_id: UUID
    answer: str = Field(min_length=1)


class SubmitAnswerResponse(BaseModel):
    session_id: UUID
    follow_up_question: dict | None


class EvaluateSessionResponse(BaseModel):
    session_id: UUID
    evaluations: list[dict]


class ReportResponse(BaseModel):
    session_id: UUID
    report: str


class GraphStatusResponse(BaseModel):
    preparation_graph_compiles: bool
    live_interview_graph_compiles: bool
