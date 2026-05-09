from typing import Protocol

from app.domain.models import CandidateProfile, InterviewPlan, JobAnalysis, SourceCitation


class CandidateProfilerAgent(Protocol):
    async def run(self) -> CandidateProfile:
        ...


class JDAnalyzerAgent(Protocol):
    async def run(self) -> JobAnalysis:
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

