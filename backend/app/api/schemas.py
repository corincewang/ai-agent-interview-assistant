from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.models import DocumentType, InterviewMode


class CreateInterviewSessionRequest(BaseModel):
    company_name: str = Field(min_length=1)
    role_title: str = Field(min_length=1)
    job_description: str = Field(min_length=1)
    mode: InterviewMode = InterviewMode.GENERAL_SWE


class CreateInterviewSessionResponse(BaseModel):
    session_id: UUID
    company_name: str
    role_title: str
    mode: InterviewMode


class UploadDocumentResponse(BaseModel):
    session_id: UUID
    document_type: DocumentType
    file_name: str


class PrepareSessionResponse(BaseModel):
    session_id: UUID
    interview_plan: dict
    interview_plan_critique: dict | None = None


class InterviewPlanResponse(BaseModel):
    session_id: UUID
    interview_plan: dict


class InterviewSessionDatabaseSummaryResponse(BaseModel):
    session_id: UUID
    company_name: str
    role_title: str
    status: str
    document_count: int
    parsed_document_count: int
    chunk_count: int
    embedded_chunk_count: int
    plan_count: int
    question_count: int


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
