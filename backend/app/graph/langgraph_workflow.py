from langgraph.graph import END, START, StateGraph

from app.graph.state import InterviewGraphState


class LangGraphInterviewWorkflow:
    async def ingest_documents(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def extract_resume_profile(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def profile_candidate(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def analyze_jd(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def research_company(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def collect_interview_intel(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

    async def plan_interview(self, state: InterviewGraphState) -> InterviewGraphState:
        return state

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
        graph.add_node("research_company", self.research_company)
        graph.add_node("collect_interview_intel", self.collect_interview_intel)
        graph.add_node("plan_interview", self.plan_interview)

        graph.add_edge(START, "ingest_documents")
        graph.add_edge("ingest_documents", "extract_resume_profile")
        graph.add_edge("extract_resume_profile", "profile_candidate")
        graph.add_edge("profile_candidate", "analyze_jd")
        graph.add_edge("analyze_jd", "research_company")
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

