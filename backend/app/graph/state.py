from dataclasses import dataclass, field
from uuid import UUID

from app.domain.models import (
    CandidateJobMatch,
    CandidateProfile,
    InterviewPlan,
    InterviewTurn,
    JobAnalysis,
    ParsedDocument,
    ResumeProfile,
    SourceCitation,
)


@dataclass
class InterviewGraphState:
    session_id: UUID
    user_id: UUID
    company_name: str
    role_title: str
    jd_text: str
    parsed_documents: list[ParsedDocument] = field(default_factory=list)
    resume_profile: ResumeProfile | None = None
    candidate_profile: CandidateProfile | None = None
    job_analysis: JobAnalysis | None = None
    candidate_job_match: CandidateJobMatch | None = None
    company_sources: list[SourceCitation] = field(default_factory=list)
    interview_intel: list[SourceCitation] = field(default_factory=list)
    interview_plan: InterviewPlan | None = None
    transcript: list[InterviewTurn] = field(default_factory=list)
    final_report: str | None = None
