from dataclasses import replace

from langgraph.graph import END, START, StateGraph

from app.agents.interview_planner import InterviewPlannerAgent
from app.graph.state import InterviewGraphState
from app.skills.contracts import InterviewPlanningSkill


class LangGraphInterviewWorkflow:
    def __init__(self, interview_planning_skill: InterviewPlanningSkill | None = None) -> None:
        self.interview_planning_skill = interview_planning_skill

    async def ingest_documents(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def extract_resume_profile(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def profile_candidate(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def analyze_jd(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def match_candidate_to_job(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def research_company(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def collect_interview_intel(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def plan_interview(self, state: InterviewGraphState) -> InterviewGraphState:
        if self.interview_planning_skill is None:
            return state

        if state.candidate_profile is None:
            raise ValueError("candidate_profile is required before planning an interview")
        if state.job_analysis is None:
            raise ValueError("job_analysis is required before planning an interview")
        if state.candidate_job_match is None:
            raise ValueError("candidate_job_match is required before planning an interview")

        agent = InterviewPlannerAgent(
            session_id=state.session_id,
            candidate_profile=state.candidate_profile,
            job_analysis=state.job_analysis,
            candidate_job_match=state.candidate_job_match,
            company_sources=state.company_sources,
            interview_intel=state.interview_intel,
            interview_planning_skill=self.interview_planning_skill,
        )
        interview_plan = await agent.run()
        return replace(state, interview_plan=interview_plan)

    async def run_live_turn(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def evaluate_session(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def generate_report(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    def build_preparation_graph(self):
        graph = StateGraph(InterviewGraphState)

        graph.add_node("ingest_documents", self.ingest_documents)
        graph.add_node("extract_resume_profile", self.extract_resume_profile)
        graph.add_node("profile_candidate", self.profile_candidate)
        graph.add_node("analyze_jd", self.analyze_jd)
        graph.add_node("match_candidate_to_job", self.match_candidate_to_job)
        graph.add_node("research_company", self.research_company)
        graph.add_node("collect_interview_intel", self.collect_interview_intel)
        graph.add_node("plan_interview", self.plan_interview)

        graph.add_edge(START, "ingest_documents")
        graph.add_edge("ingest_documents", "extract_resume_profile")
        graph.add_edge("extract_resume_profile", "profile_candidate")
        graph.add_edge("profile_candidate", "analyze_jd")
        graph.add_edge("analyze_jd", "match_candidate_to_job")
        graph.add_edge("match_candidate_to_job", "research_company")
        graph.add_edge("research_company", "collect_interview_intel")
        graph.add_edge("collect_interview_intel", "plan_interview")
        graph.add_edge("plan_interview", END)

        return graph.compile()

    def build_live_interview_graph(self):
        graph = StateGraph(InterviewGraphState)

        graph.add_node("run_live_turn", self.run_live_turn)
        graph.add_node("evaluate_session", self.evaluate_session)
        graph.add_node("generate_report", self.generate_report)

        graph.add_edge(START, "run_live_turn")
        graph.add_edge("run_live_turn", "evaluate_session")
        graph.add_edge("evaluate_session", "generate_report")
        graph.add_edge("generate_report", END)

        return graph.compile()
