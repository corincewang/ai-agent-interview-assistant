from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Literal
from uuid import UUID, uuid4


class DocumentType(str, Enum):
    RESUME = "resume"
    KNOWLEDGE_BASE = "knowledge_base"
    JOB_DESCRIPTION = "job_description"
    COMPANY_RESEARCH = "company_research"
    INTERVIEW_INTEL = "interview_intel"


class InterviewMode(str, Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    AI_AGENT = "ai_agent"
    GENERAL_SWE = "general_swe"


class InterviewTurnRole(str, Enum):
    INTERVIEWER = "interviewer"
    CANDIDATE = "candidate"
    SYSTEM = "system"


@dataclass(frozen=True)
class DocumentInput:
    file_path: Path
    document_type: DocumentType
    document_id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class SourceCitation:
    title: str
    url: str | None
    source_type: DocumentType
    confidence: float


@dataclass(frozen=True)
class ResearchFinding:
    citation: SourceCitation
    summary: str
    relevant_topics: list[str]
    extracted_signals: list[str]


@dataclass(frozen=True)
class SourceSpan:
    document_id: UUID
    page_number: int | None
    start_char: int | None
    end_char: int | None
    text_excerpt: str


@dataclass(frozen=True)
class ParsedDocument:
    id: UUID
    document_type: DocumentType
    raw_text: str
    source_spans: list[SourceSpan]
    metadata: dict[str, Any]


@dataclass(frozen=True)
class DocumentChunk:
    id: UUID
    document_id: UUID
    text: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class EmbeddedDocumentChunk:
    chunk: DocumentChunk
    embedding: list[float]
    embedding_model: str


@dataclass(frozen=True)
class KnowledgeIndexingResult:
    session_id: UUID
    indexed_document_ids: list[UUID]
    indexed_chunk_ids: list[UUID]
    skipped_document_ids: list[UUID]
    warnings: list[str]


@dataclass(frozen=True)
class RetrievedKnowledgeChunk:
    chunk: DocumentChunk
    score: float
    rank: int
    retrieval_query: str


@dataclass(frozen=True)
class KnowledgeRetrievalResult:
    session_id: UUID
    query: str
    chunks: list[RetrievedKnowledgeChunk]
    warnings: list[str]


@dataclass(frozen=True)
class EducationItem:
    institution: str
    degree: str
    majors: list[str]
    minors: list[str]
    graduation_date: str | None
    gpa: str | None
    evidence: list[SourceSpan]


@dataclass(frozen=True)
class SkillInventory:
    programming_languages: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)
    cloud_and_devops: list[str] = field(default_factory=list)
    databases: list[str] = field(default_factory=list)
    ai_agent_stack: list[str] = field(default_factory=list)
    mobile_stack: list[str] = field(default_factory=list)
    testing_stack: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class LanguageProficiency:
    language: str
    level: str
    evidence: list[SourceSpan]


@dataclass(frozen=True)
class QuantifiedImpact:
    metric: str
    value: str
    context: str
    evidence: list[SourceSpan]


@dataclass(frozen=True)
class WorkExperience:
    company: str
    location: str | None
    title: str
    employment_type: str | None
    start_date: str | None
    end_date: str | None
    responsibilities: list[str]
    technologies: list[str]
    quantified_impacts: list[QuantifiedImpact]
    evidence: list[SourceSpan]


@dataclass(frozen=True)
class ProjectExperience:
    name: str
    role: str | None
    start_date: str | None
    end_date: str | None
    summary: str
    technologies: list[str]
    architecture_notes: list[str]
    quantified_impacts: list[QuantifiedImpact]
    links: list[str]
    evidence: list[SourceSpan]


@dataclass(frozen=True)
class ResumeProfile:
    user_id: UUID
    name: str | None
    education: list[EducationItem]
    skills: SkillInventory
    languages: list[LanguageProficiency]
    work_experiences: list[WorkExperience]
    project_experiences: list[ProjectExperience]
    portfolio_links: list[str]
    extraction_warnings: list[str]


@dataclass(frozen=True)
class CandidateProfile:
    user_id: UUID
    resume_profile: ResumeProfile
    technical_skills: list[str]
    project_highlights: list[str]
    risk_areas: list[str]
    follow_up_targets: list[str]
    strongest_signals: list[str]
    interview_positioning: str
    evidence: list[SourceSpan | SourceCitation]


@dataclass(frozen=True)
class JobAnalysis:
    company_name: str
    role_title: str
    required_skills: list[str]
    preferred_skills: list[str]
    responsibilities: list[str]


@dataclass(frozen=True)
class CandidateJobMatch:
    session_id: UUID
    candidate_matches: list[str]
    candidate_gaps: list[str]
    role_specific_risk_areas: list[str]
    recommended_positioning: str


@dataclass(frozen=True)
class InterviewQuestion:
    id: UUID
    prompt: str
    topic: str
    difficulty: Literal["easy", "medium", "hard"]
    expected_signals: list[str]
    follow_up_strategy: list[str]


@dataclass(frozen=True)
class InterviewPlan:
    session_id: UUID
    mode: InterviewMode
    questions: list[InterviewQuestion]
    rubric: dict[str, str]
    candidate_storyline: str
    planned_deep_dives: list[str]


@dataclass(frozen=True)
class QuestionCritique:
    question_id: UUID
    resume_grounding_score: float
    jd_coverage_score: float
    rag_grounding_score: float
    specificity_score: float
    follow_up_potential_score: float
    overall_score: float
    strengths: list[str]
    improvement_suggestions: list[str]


@dataclass(frozen=True)
class InterviewPlanCritique:
    session_id: UUID
    overall_score: float
    quality_gate_passed: bool
    question_critiques: list[QuestionCritique]
    coverage_summary: dict[str, str]
    revision_recommendations: list[str]


@dataclass(frozen=True)
class InterviewTurn:
    session_id: UUID
    role: InterviewTurnRole
    content: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class AnswerEvaluation:
    turn_id: UUID
    scores: dict[str, float]
    strengths: list[str]
    weaknesses: list[str]
    improved_answer: str
    next_practice_steps: list[str]
