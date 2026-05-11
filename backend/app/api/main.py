from pathlib import Path
from uuid import UUID

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.api.schemas import (
    CreateInterviewSessionRequest,
    CreateInterviewSessionResponse,
    EvaluateSessionResponse,
    GraphStatusResponse,
    InterviewPlanResponse,
    InterviewSessionDatabaseSummaryResponse,
    PrepareSessionResponse,
    ReportResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
    UploadDocumentResponse,
)
from app.domain.models import DocumentType
from app.graph.langgraph_workflow import LangGraphInterviewWorkflow
from app.services.interview_service import InterviewService
from app.services.session_store import InMemoryInterviewSessionStore
from app.utils.serialization import to_jsonable


app = FastAPI(
    title="AI Agent Interview Assistant API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = InMemoryInterviewSessionStore()
interview_service = InterviewService(store)
UPLOAD_ROOT = Path("/private/tmp/ai-agent-interview-assistant")

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/interview-sessions", response_model=CreateInterviewSessionResponse)
async def create_interview_session(
    request: CreateInterviewSessionRequest,
) -> CreateInterviewSessionResponse:
    session = await interview_service.create_session(
        company_name=request.company_name,
        role_title=request.role_title,
        jd_text=request.job_description,
        mode=request.mode,
    )
    return CreateInterviewSessionResponse(
        session_id=session.session_id,
        company_name=session.company_name,
        role_title=session.role_title,
        mode=session.mode,
    )


@app.post(
    "/interview-sessions/{session_id}/documents",
    response_model=UploadDocumentResponse,
)
async def upload_document(
    session_id: UUID,
    document_type: DocumentType,
    file: UploadFile = File(...),
) -> UploadDocumentResponse:
    try:
        store.require_session(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    session_dir = UPLOAD_ROOT / str(session_id)
    session_dir.mkdir(parents=True, exist_ok=True)
    file_name = file.filename or "uploaded_document"
    file_path = session_dir / file_name
    file_path.write_bytes(await file.read())

    await interview_service.add_document(
        session_id=session_id,
        file_path=file_path,
        document_type=document_type,
    )
    return UploadDocumentResponse(
        session_id=session_id,
        document_type=document_type,
        file_name=file_name,
    )


@app.post(
    "/interview-sessions/{session_id}/prepare",
    response_model=PrepareSessionResponse,
)
async def prepare_interview_session(session_id: UUID) -> PrepareSessionResponse:
    try:
        interview_plan = await interview_service.prepare_session(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return PrepareSessionResponse(
        session_id=session_id,
        interview_plan=to_jsonable(interview_plan),
        interview_plan_critique=to_jsonable(
            store.require_session(session_id).prepared_state.get("interview_plan_critique")
        ),
    )


@app.get(
    "/interview-sessions/{session_id}/interview-plan",
    response_model=InterviewPlanResponse,
)
async def get_interview_plan(session_id: UUID) -> InterviewPlanResponse:
    try:
        interview_plan = await interview_service.get_interview_plan_payload(session_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return InterviewPlanResponse(
        session_id=session_id,
        interview_plan=interview_plan,
    )


@app.get(
    "/interview-sessions/{session_id}/db-summary",
    response_model=InterviewSessionDatabaseSummaryResponse,
)
async def get_interview_session_database_summary(
    session_id: UUID,
) -> InterviewSessionDatabaseSummaryResponse:
    summary = await interview_service.persistence.get_session_summary(session_id)
    if summary is None:
        raise HTTPException(status_code=404, detail=f"Interview session not found: {session_id}")

    return InterviewSessionDatabaseSummaryResponse(
        session_id=summary.session_id,
        company_name=summary.company_name,
        role_title=summary.role_title,
        status=summary.status,
        document_count=summary.document_count,
        parsed_document_count=summary.parsed_document_count,
        chunk_count=summary.chunk_count,
        embedded_chunk_count=summary.embedded_chunk_count,
        plan_count=summary.plan_count,
        question_count=summary.question_count,
        critique_count=summary.critique_count,
        critique_overall_score=summary.critique_overall_score,
        critique_quality_gate_passed=summary.critique_quality_gate_passed,
    )


@app.post(
    "/interview-sessions/{session_id}/turns",
    response_model=SubmitAnswerResponse,
)
async def submit_answer(
    session_id: UUID,
    request: SubmitAnswerRequest,
) -> SubmitAnswerResponse:
    try:
        follow_up = await interview_service.submit_answer(
            session_id=session_id,
            question_id=request.question_id,
            answer=request.answer,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return SubmitAnswerResponse(
        session_id=session_id,
        follow_up_question=to_jsonable(follow_up) if follow_up else None,
    )


@app.post(
    "/interview-sessions/{session_id}/evaluate",
    response_model=EvaluateSessionResponse,
)
async def evaluate_interview_session(session_id: UUID) -> EvaluateSessionResponse:
    try:
        evaluations = await interview_service.evaluate_session(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return EvaluateSessionResponse(
        session_id=session_id,
        evaluations=to_jsonable(evaluations),
    )


@app.post(
    "/interview-sessions/{session_id}/report",
    response_model=ReportResponse,
)
async def generate_report(session_id: UUID) -> ReportResponse:
    try:
        report = await interview_service.generate_report(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ReportResponse(session_id=session_id, report=report)


@app.get(
    "/interview-sessions/{session_id}/report",
    response_model=ReportResponse,
)
async def get_report(session_id: UUID) -> ReportResponse:
    try:
        report = interview_service.get_report(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ReportResponse(session_id=session_id, report=report)


@app.get("/graph/status", response_model=GraphStatusResponse)
async def graph_status() -> GraphStatusResponse:
    workflow = LangGraphInterviewWorkflow()
    workflow.build_preparation_graph()
    workflow.build_live_interview_graph()

    return GraphStatusResponse(
        preparation_graph_compiles=True,
        live_interview_graph_compiles=True,
    )
