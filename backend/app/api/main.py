from uuid import UUID, uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.domain.models import InterviewMode
from app.graph.langgraph_workflow import LangGraphInterviewWorkflow


app = FastAPI(
    title="AI Agent Interview Assistant API",
    version="0.1.0",
)


class CreateInterviewSessionRequest(BaseModel):
    company_name: str = Field(min_length=1)
    role_title: str = Field(min_length=1)
    job_description: str = Field(min_length=1)
    mode: InterviewMode = InterviewMode.GENERAL_SWE


class CreateInterviewSessionResponse(BaseModel):
    session_id: UUID
    company_name: str
    role_title: str
    mode: InterviewMode


class GraphStatusResponse(BaseModel):
    preparation_graph_compiles: bool
    live_interview_graph_compiles: bool


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/interview-sessions", response_model=CreateInterviewSessionResponse)
async def create_interview_session(
    request: CreateInterviewSessionRequest,
) -> CreateInterviewSessionResponse:
    return CreateInterviewSessionResponse(
        session_id=uuid4(),
        company_name=request.company_name,
        role_title=request.role_title,
        mode=request.mode,
    )


@app.get("/graph/status", response_model=GraphStatusResponse)
async def graph_status() -> GraphStatusResponse:
    workflow = LangGraphInterviewWorkflow()
    workflow.build_preparation_graph()
    workflow.build_live_interview_graph()

    return GraphStatusResponse(
        preparation_graph_compiles=True,
        live_interview_graph_compiles=True,
    )

