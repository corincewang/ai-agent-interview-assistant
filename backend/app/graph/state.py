from dataclasses import dataclass, field
from uuid import UUID

from app.domain.models import (
    CandidateJobMatch,
    CandidateProfile,
    DocumentChunk,
    DocumentInput,
    InterviewPlan,
    InterviewTurn,
    JobAnalysis,
    ParsedDocument,
    ResearchFinding,
    ResumeProfile,
)


@dataclass
class InterviewGraphState:
    session_id: UUID
    user_id: UUID
    company_name: str
    role_title: str
    jd_text: str
    document_inputs: list[DocumentInput] = field(default_factory=list)
    parsed_documents: list[ParsedDocument] = field(default_factory=list)
    document_chunks: list[DocumentChunk] = field(default_factory=list)
    resume_profile: ResumeProfile | None = None
    candidate_profile: CandidateProfile | None = None
    job_analysis: JobAnalysis | None = None
    candidate_job_match: CandidateJobMatch | None = None
    company_sources: list[ResearchFinding] = field(default_factory=list)
    interview_intel: list[ResearchFinding] = field(default_factory=list)
    interview_plan: InterviewPlan | None = None
    transcript: list[InterviewTurn] = field(default_factory=list)
    final_report: str | None = None
