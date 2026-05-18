import json
from collections.abc import AsyncIterator
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.api.schemas import (
    BatchUploadDocumentsResponse,
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
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1|172\.\d+\.\d+\.\d+)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = InMemoryInterviewSessionStore()
interview_service = InterviewService(store)
UPLOAD_ROOT = Path("/private/tmp/ai-agent-interview-assistant")
SUPPORTED_BATCH_UPLOAD_SUFFIXES = {".pdf"}


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
        target_track=request.target_track,
        jd_text=request.jd_text or "",
        mode=request.mode,
    )
    return CreateInterviewSessionResponse(
        session_id=session.session_id,
        company_name=session.company_name,
        role_title=session.role_title,
        target_track=session.target_track,
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
    file_path = _safe_upload_path(session_dir, file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)
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
    "/interview-sessions/{session_id}/documents/batch",
    response_model=BatchUploadDocumentsResponse,
)
async def upload_documents_batch(
    session_id: UUID,
    document_type: DocumentType,
    files: list[UploadFile] = File(...),
) -> BatchUploadDocumentsResponse:
    try:
        store.require_session(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if not files:
        raise HTTPException(status_code=400, detail="At least one PDF file is required.")

    rejected_file_names = [
        file.filename or "uploaded_document.pdf"
        for file in files
        if Path(file.filename or "uploaded_document.pdf").suffix.lower()
        not in SUPPORTED_BATCH_UPLOAD_SUFFIXES
    ]
    if rejected_file_names:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Batch upload currently supports PDF files only.",
                "rejected_file_names": rejected_file_names,
            },
        )

    batch_dir = UPLOAD_ROOT / str(session_id) / "batch" / str(uuid4())
    batch_dir.mkdir(parents=True, exist_ok=True)

    for file in files:
        file_name = file.filename or "uploaded_document.pdf"
        file_path = _safe_upload_path(batch_dir, file_name)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(await file.read())

    document_inputs = await interview_service.add_documents_from_path(
        session_id=session_id,
        root_path=batch_dir,
        document_type=document_type,
        suffixes=SUPPORTED_BATCH_UPLOAD_SUFFIXES,
    )

    return BatchUploadDocumentsResponse(
        session_id=session_id,
        document_type=document_type,
        document_count=len(document_inputs),
        file_names=[document_input.file_path.name for document_input in document_inputs],
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
        revised=interview_plan.revised,
        revision_attempts_used=interview_plan.revision_attempts_used,
    )


@app.post("/interview-sessions/{session_id}/prepare/stream")
async def prepare_interview_session_stream(session_id: UUID) -> StreamingResponse:
    async def event_stream() -> AsyncIterator[str]:
        try:
            store.require_session(session_id)
            async for event in interview_service.prepare_session_events(session_id):
                event_name = str(event.pop("event"))
                yield _sse_event(event_name, event)
        except KeyError as exc:
            yield _sse_event("error", {"message": str(exc), "status_code": 404})
        except ValueError as exc:
            yield _sse_event("error", {"message": str(exc), "status_code": 400})

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
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

    revised = bool(interview_plan.get("revised", False))
    revision_attempts_used_raw = interview_plan.get("revision_attempts_used", 0)
    try:
        revision_attempts_used = int(revision_attempts_used_raw)
    except (TypeError, ValueError):
        revision_attempts_used = 0

    return InterviewPlanResponse(
        session_id=session_id,
        interview_plan=interview_plan,
        revised=revised,
        revision_attempts_used=revision_attempts_used,
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
        target_track=summary.target_track,
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


def _safe_upload_path(root: Path, file_name: str) -> Path:
    safe_parts = [
        part
        for part in Path(file_name).parts
        if part not in {"", ".", ".."} and not Path(part).is_absolute()
    ]
    if not safe_parts:
        safe_parts = ["uploaded_document.pdf"]

    candidate = (root / Path(*safe_parts)).resolve()
    resolved_root = root.resolve()
    if not candidate.is_relative_to(resolved_root):
        raise HTTPException(status_code=400, detail=f"Unsafe upload path: {file_name}")

    return candidate


def _sse_event(event_name: str, payload: dict) -> str:
    return (
        f"event: {event_name}\n"
        f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
    )
