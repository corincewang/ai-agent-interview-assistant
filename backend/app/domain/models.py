from dataclasses import dataclass
from enum import Enum
from typing import Any, Literal
from uuid import UUID


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
class SourceCitation:
    title: str
    url: str | None
    source_type: DocumentType
    confidence: float


@dataclass(frozen=True)
class DocumentChunk:
    id: UUID
    document_id: UUID
    text: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class CandidateProfile:
    user_id: UUID
    technical_skills: list[str]
    project_highlights: list[str]
    risk_areas: list[str]
    follow_up_targets: list[str]
    evidence: list[SourceCitation]


@dataclass(frozen=True)
class JobAnalysis:
    company_name: str
    role_title: str
    required_skills: list[str]
    preferred_skills: list[str]
    responsibilities: list[str]
    candidate_matches: list[str]
    candidate_gaps: list[str]


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

