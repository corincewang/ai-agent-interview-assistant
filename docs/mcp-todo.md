# MCP To-Do List

## Phase 0: Contract Design

- Define MCP server boundaries.
- Define tool input and output schemas.
- Define skill-level orchestration contracts.
- Define LangGraph state schema.
- Define persistence models for sessions, documents, turns, and reports.
- Define frontend API contracts.

## Phase 1: Local MVP Tools

- `parse_document`: Extract text from resume and knowledge base files.
- `chunk_document`: Split extracted text into retrievable chunks.
- `embed_chunks`: Generate embeddings for document chunks.
- `retrieve_context`: Search resume, JD, and knowledge base context.
- `save_interview_turn`: Persist each interview question and answer.
- `load_interview_session`: Load the active interview state.

## Phase 2: Agent Skills

- `candidate_profiling_skill`: Build candidate profile from resume and knowledge base.
- `jd_analysis_skill`: Extract skills, responsibilities, and gaps from JD.
- `interview_planning_skill`: Generate question plan and rubric.
- `live_interview_skill`: Ask questions and decide follow-ups.
- `evaluation_skill`: Score answers using role-aware rubrics.
- `report_generation_skill`: Generate final feedback and training plan.

## Phase 3: External Research MCP

- `company_search`: Search public company and role information.
- `fetch_public_page`: Fetch readable source text from public URLs.
- `summarize_source`: Summarize source with citation metadata.
- `score_source_confidence`: Estimate source relevance and reliability.
- `interview_intel_search`: Search public interview experience summaries.

## Phase 4: Voice MCP

- `transcribe_audio`: Convert user speech to text.
- `synthesize_speech`: Convert interviewer text to speech.
- `stream_interview_events`: Stream transcript and state updates.

## Phase 5: Production Hardening

- Add rate limiting.
- Add source compliance checks.
- Add observability for each agent node.
- Add cost and latency tracking.
- Add user data deletion workflow.
- Add prompt/version audit trails.

