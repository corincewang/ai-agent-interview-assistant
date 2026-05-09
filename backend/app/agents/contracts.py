from typing import Protocol

from app.domain.models import (
    CandidateJobMatch,
    CandidateProfile,
    InterviewPlan,
    JobAnalysis,
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
    async def run(self) -> list[SourceCitation]:
        ...


class InterviewIntelAgent(Protocol):
    async def run(self) -> list[SourceCitation]:
        ...


class InterviewPlannerAgent(Protocol):
    async def run(self) -> InterviewPlan:
        ...


class LiveInterviewerAgent(Protocol):
    async def run_turn(self) -> str:
        ...


class EvaluatorAgent(Protocol):
    async def run(self) -> str:
        ...
