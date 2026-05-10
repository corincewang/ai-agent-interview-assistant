from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.domain.models import (
    AnswerEvaluation,
    DocumentInput,
    InterviewMode,
    InterviewPlan,
    InterviewTurn,
)


@dataclass
class InterviewSessionRecord:
    session_id: UUID
    user_id: UUID
    company_name: str
    role_title: str
    jd_text: str
    mode: InterviewMode
    document_inputs: list[DocumentInput] = field(default_factory=list)
    prepared_state: dict | None = None
    interview_plan: InterviewPlan | None = None
    transcript: list[InterviewTurn] = field(default_factory=list)
    evaluations: list[AnswerEvaluation] = field(default_factory=list)
    report: str | None = None


class InMemoryInterviewSessionStore:
    def __init__(self) -> None:
        self._sessions: dict[UUID, InterviewSessionRecord] = {}

    def create_session(
        self,
        company_name: str,
        role_title: str,
        jd_text: str,
        mode: InterviewMode,
    ) -> InterviewSessionRecord:
        session = InterviewSessionRecord(
            session_id=uuid4(),
            user_id=uuid4(),
            company_name=company_name,
            role_title=role_title,
            jd_text=jd_text,
            mode=mode,
        )
        self._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: UUID) -> InterviewSessionRecord | None:
        return self._sessions.get(session_id)

    def require_session(self, session_id: UUID) -> InterviewSessionRecord:
        session = self.get_session(session_id)
        if session is None:
            raise KeyError(f"Interview session not found: {session_id}")
        return session

