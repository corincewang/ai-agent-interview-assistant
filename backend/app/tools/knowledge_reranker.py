"""Cross-encoder reranking for RAG retrieval (FlashRank ONNX, no Torch)."""

from __future__ import annotations

import os
import threading
from dataclasses import replace

from flashrank import Ranker, RerankRequest

from app.domain.models import RetrievedKnowledgeChunk

# Multilingual-ish MS MARCO cross-encoder; override with FLASHRANK_MODEL_NAME, e.g. ms-marco-MiniLM-L-12-v2.
_DEFAULT_FLASHRANK_MODEL = "ms-marco-MultiBERT-L-12"
_MAX_CHARS_PER_PASSAGE = 12_000

_lock = threading.Lock()
_ranker: Ranker | None = None


def _get_ranker() -> Ranker:
    global _ranker  # noqa: PLW0603 — process-local singleton
    raw = os.getenv("FLASHRANK_MODEL_NAME", _DEFAULT_FLASHRANK_MODEL).strip()
    model_name = raw or _DEFAULT_FLASHRANK_MODEL
    with _lock:
        if _ranker is None:
            _ranker = Ranker(model_name=model_name, max_length=512)
        return _ranker


def rerank_retrieved_chunks(
    query: str,
    chunks: list[RetrievedKnowledgeChunk],
) -> list[RetrievedKnowledgeChunk]:
    """Reorder chunks by cross-encoder relevance; updates ``score`` and ``rank`` (1-based).

    Keeps chunk identity and metadata; ignores entries FlashRank drops (unlikely if ids unique).
    """
    if len(chunks) <= 1:
        return [_with_rank(score=c.score, chunk=c, idx=i) for i, c in enumerate(chunks)]

    passages = [{"id": str(c.chunk.id), "text": c.chunk.text[:_MAX_CHARS_PER_PASSAGE]} for c in chunks]
    rerank_req = RerankRequest(query=query, passages=passages)

    ranked = _get_ranker().rerank(rerank_req)
    by_chunk_id = {str(c.chunk.id): c for c in chunks}
    reranked: list[RetrievedKnowledgeChunk] = []
    for idx, row in enumerate(ranked):
        orig = by_chunk_id.get(row["id"])
        if orig is None:
            continue
        reranked.append(_with_rank(score=float(row["score"]), chunk=orig, idx=idx))

    if len(reranked) < len(chunks):
        seen = {str(r.chunk.id) for r in reranked}
        fallback_rank = len(reranked)
        for c in chunks:
            if str(c.chunk.id) not in seen:
                fallback_rank += 1
                reranked.append(_with_rank(score=c.score, chunk=c, idx=fallback_rank - 1))

    return reranked


def _with_rank(*, score: float, chunk: RetrievedKnowledgeChunk, idx: int) -> RetrievedKnowledgeChunk:
    return replace(chunk, score=score, rank=idx + 1)
