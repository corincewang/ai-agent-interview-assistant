from typing import Protocol

from app.domain.models import (
    CandidateJobMatch,
    CandidateProfile,
    InterviewPlan,
    JobAnalysis,
    ResearchFinding,
    ResumeProfile,
    SourceCitation,
)


class ResumeExtractorAgent(Protocol):
    async def run(self) -> ResumeProfile:
        ...


class CandidateProfilerAgent(Protocol):
    async def run(self) -> CandidateProfile:
        ...


class JDAnalyzerAgent(Protocol):
    async def run(self) -> JobAnalysis:
        ...


class CandidateJobMatcherAgent(Protocol):
    async def run(self) -> CandidateJobMatch:
        ...


class CompanyResearchAgent(Protocol):
    async def run(self) -> list[ResearchFinding]:
        ...


class InterviewIntelAgent(Protocol):
    async def run(self) -> list[ResearchFinding]:
        ...


class InterviewPlannerAgent(Protocol):
    async def run(self) -> InterviewPlan:
        ...


class LiveInterviewerAgent(Protocol):
    async def select_next_question(self) -> InterviewQuestion:
        ...

    async def decide_follow_up(
        self,
        current_question: InterviewQuestion,
        candidate_answer: str,
    ) -> InterviewQuestion | None:
        ...


class EvaluatorAgent(Protocol):
    async def run(self) -> AnswerEvaluation:
        ...


class ReportGeneratorAgent(Protocol):
    async def run(self) -> str:
        ...
