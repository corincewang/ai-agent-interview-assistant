from typing import Protocol

from app.graph.state import InterviewGraphState


class InterviewWorkflow(Protocol):
    async def ingest_documents(self, state: InterviewGraphState) -> InterviewGraphState:
        ...

    async def profile_candidate(self, state: InterviewGraphState) -> InterviewGraphState:
        ...

    async def analyze_jd(self, state: InterviewGraphState) -> InterviewGraphState:
        ...

    async def research_company(self, state: InterviewGraphState) -> InterviewGraphState:
        ...

    async def collect_interview_intel(self, state: InterviewGraphState) -> InterviewGraphState:
        ...

    async def plan_interview(self, state: InterviewGraphState) -> InterviewGraphState:
        ...

    async def run_live_turn(self, state: InterviewGraphState) -> InterviewGraphState:
        ...

    async def evaluate_session(self, state: InterviewGraphState) -> InterviewGraphState:
        ...

    async def generate_report(self, state: InterviewGraphState) -> InterviewGraphState:
        ...

