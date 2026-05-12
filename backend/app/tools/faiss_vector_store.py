"""FAISS via LangChain, keyed by ``session_id``.

**Persistence.** Set ``FAISS_PERSIST_DIRECTORY`` (see ``Settings``). Each interview session owns a
directory ``<persist>/<uuid>/`` containing LangChain defaults ``index.faiss`` + ``index.pkl``.
On first access we ``load_local`` if present; after each upsert batch we ``save_local``.

**PostgreSQL + FAISS (hybrid).** Use Postgres for relational data (sessions, documents, transcripts)
and optionally ``pgvector`` for server-side embeddings; **in parallel**, ``VECTOR_STORE_BACKEND=faiss``
can keep a Faiss corpus on disk for this API's RAG prepare path — the durable link between them is the
same ``session_id`` (UUID folder name equals ``interview_sessions.id``). Postgres does not ingest the
``*.faiss`` / ``*.pkl`` bytes unless you explicitly add blob columns later.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any
from uuid import UUID

import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from app.db.models import EMBEDDING_DIMENSIONS
from app.domain.models import (
    DocumentChunk,
    DocumentType,
    EmbeddedDocumentChunk,
    RetrievedKnowledgeChunk,
)

_INDEX_NAME_DEFAULT = "index"


class _PrecomputedEmbeddings(Embeddings):
    """Minimal ``Embeddings`` instance required by LangChain ``FAISS``; vectors come from ``add_embeddings``."""

    def __init__(self, dimension: int) -> None:
        self.dimension = dimension

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        raise RuntimeError("Use ``add_embeddings`` only.")

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        raise RuntimeError("Use ``add_embeddings`` only.")

    def embed_query(self, text: str) -> list[float]:
        raise RuntimeError("Use ``similarity_search_*_by_vector`` with precomputed query embeddings.")

    async def aembed_query(self, text: str) -> list[float]:
        raise RuntimeError("Use ``similarity_search_*_by_vector`` with precomputed query embeddings.")


def _lc_faiss_for_dimension(dimension: int) -> FAISS:
    index = faiss.IndexFlatIP(dimension)
    return FAISS(
        embedding_function=_PrecomputedEmbeddings(dimension),
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
        normalize_L2=False,
        distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT,
    )


def _chunk_metadata_lc(embedded: EmbeddedDocumentChunk) -> dict[str, str]:
    core = dict(embedded.chunk.metadata)
    core.setdefault("embedding_model", embedded.embedding_model)
    dt = core.get("document_type")
    if dt is None:
        dt = ""
    return {
        "__chunk_uuid__": str(embedded.chunk.id),
        "__document_uuid__": str(embedded.chunk.document_id),
        "document_type": str(dt),
        "__chunk_json__": json.dumps(core, default=str),
    }


def _document_chunk_from_lc(doc: Document) -> DocumentChunk:
    merged = json.loads(str(doc.metadata["__chunk_json__"]))
    return DocumentChunk(
        id=UUID(str(doc.metadata["__chunk_uuid__"])),
        document_id=UUID(str(doc.metadata["__document_uuid__"])),
        text=doc.page_content,
        metadata=merged,
    )


def _filter_fn_for_search(
    document_types: list[DocumentType] | None,
    extra_filters: dict[str, Any] | None,
) -> Any | None:
    allowed = (
        None
        if not document_types
        else {t.value if isinstance(t, DocumentType) else str(t) for t in document_types}
    )

    def _predicate(meta: dict) -> bool:
        if allowed is not None:
            mt = meta.get("document_type")
            if mt not in allowed:
                return False

        if not extra_filters:
            return True

        inner_raw = meta.get("__chunk_json__")
        if not isinstance(inner_raw, str):
            return False
        try:
            blob = json.loads(inner_raw)
        except json.JSONDecodeError:
            return False

        for key, expected in extra_filters.items():
            observed = blob.get(key)
            if isinstance(expected, UUID):
                try:
                    if UUID(str(observed)) != expected:
                        return False
                except ValueError:
                    return False
            elif str(observed) != str(expected):
                return False

        return True

    if allowed is None and not extra_filters:
        return None
    return _predicate


class FaissVectorStore:
    def __init__(
        self,
        embedding_dimension: int = EMBEDDING_DIMENSIONS,
        *,
        persist_directory: Path | None = None,
        allow_local_index_pickles: bool = True,
        index_name: str = _INDEX_NAME_DEFAULT,
    ) -> None:
        if embedding_dimension <= 0:
            raise ValueError("embedding_dimension must be positive")

        self._embedding_dimension = embedding_dimension
        self._persist_directory = persist_directory
        self._allow_local_index_pickles = allow_local_index_pickles
        self._index_name = index_name
        self._lock = threading.Lock()
        self._sessions: dict[UUID, FAISS] = {}

    @property
    def embedding_dimension(self) -> int:
        return self._embedding_dimension

    @property
    def persist_directory(self) -> Path | None:
        return self._persist_directory

    def _session_paths(self, session_id: UUID) -> tuple[Path, Path]:
        """Return ``(directory, marker_faiss_path)``. ``persist_directory`` must be configured."""
        if self._persist_directory is None:
            raise RuntimeError("persist_directory is not configured.")

        resolved_root = self._persist_directory.expanduser().resolve()
        folder = resolved_root / str(session_id)
        return folder, folder / f"{self._index_name}.faiss"

    def _try_load_lc(self, session_id: UUID) -> FAISS | None:
        if self._persist_directory is None or not self._allow_local_index_pickles:
            return None

        _, faiss_marker = self._session_paths(session_id)
        folder = faiss_marker.parent

        if not faiss_marker.is_file():
            return None

        pkl_marker = folder / f"{self._index_name}.pkl"
        if not pkl_marker.is_file():
            return None

        loaded = FAISS.load_local(
            str(folder),
            embeddings=_PrecomputedEmbeddings(self._embedding_dimension),
            index_name=self._index_name,
            allow_dangerous_deserialization=self._allow_local_index_pickles,
            distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT,
            normalize_L2=False,
        )
        loaded_dim = getattr(loaded.index, "d", None)
        if isinstance(loaded_dim, int) and loaded_dim != self._embedding_dimension:
            raise ValueError(
                "Loaded Faiss dimension "
                f"{loaded_dim} != expected {self._embedding_dimension}; "
                f"inspect {folder}"
            )

        return loaded

    def _persist_lc_disk(self, session_id: UUID, lc: FAISS) -> None:
        if self._persist_directory is None:
            return
        if not self._allow_local_index_pickles:
            return

        folder, _ = self._session_paths(session_id)
        folder.mkdir(parents=True, exist_ok=True)
        lc.save_local(str(folder.resolve()), index_name=self._index_name)

    def _get_or_create_lc(self, session_id: UUID, inferred_dim_from_batch: int) -> FAISS:
        lc = self._sessions.get(session_id)
        if lc is not None:
            return lc

        loaded = self._try_load_lc(session_id)
        if loaded is not None:
            self._sessions[session_id] = loaded
            return loaded

        if inferred_dim_from_batch != self._embedding_dimension:
            raise ValueError(
                f"Inferred embedding dimension {inferred_dim_from_batch} mismatches configured "
                f"{self._embedding_dimension}"
            )
        fresh = _lc_faiss_for_dimension(self._embedding_dimension)
        self._sessions[session_id] = fresh
        return fresh

    async def upsert_chunks(
        self,
        session_id: UUID,
        chunks: list[EmbeddedDocumentChunk],
    ) -> list[UUID]:
        if not chunks:
            return []

        inferred_dim = len(chunks[0].embedding)

        with self._lock:
            lc = self._get_or_create_lc(session_id, inferred_dim)
            if inferred_dim != self._embedding_dimension:
                raise ValueError(
                    f"Chunk embedding length {inferred_dim} mismatches configured "
                    f"{self._embedding_dimension}"
                )

            known = set(lc.index_to_docstore_id.values())

            for embedded in chunks:
                cid = str(embedded.chunk.id)
                if cid in known:
                    lc.delete(ids=[cid])
                    known.remove(cid)
                lc.add_embeddings(
                    text_embeddings=[(embedded.chunk.text, embedded.embedding)],
                    metadatas=[_chunk_metadata_lc(embedded)],
                    ids=[cid],
                )
                known.add(cid)

            self._persist_lc_disk(session_id, lc)

            return [c.chunk.id for c in chunks]

    async def search(
        self,
        session_id: UUID,
        query_embedding: list[float],
        top_k: int,
        document_types: list[DocumentType] | None = None,
        filters: dict[str, Any] | None = None,
    ) -> list[RetrievedKnowledgeChunk]:
        if top_k <= 0:
            return []

        inferred_dim = len(query_embedding)

        with self._lock:
            lc = None
            if session_id in self._sessions:
                lc = self._sessions[session_id]
            elif self._persist_directory is not None:
                lc_loaded = self._try_load_lc(session_id)
                if lc_loaded is not None:
                    self._sessions[session_id] = lc_loaded
                    lc = lc_loaded

            if lc is None:
                return []

            if inferred_dim != self._embedding_dimension:
                raise ValueError(
                    f"Query embedding length {inferred_dim} mismatches configured "
                    f"{self._embedding_dimension}"
                )

            if lc.index.ntotal == 0:
                return []

            ntotal = lc.index.ntotal
            fetch_k = min(ntotal, max(top_k * 40, top_k))
            flt = _filter_fn_for_search(document_types, filters)

            rows = lc.similarity_search_with_score_by_vector(
                embedding=query_embedding,
                k=top_k,
                filter=flt,
                fetch_k=fetch_k,
            )

        return [
            RetrievedKnowledgeChunk(
                chunk=_document_chunk_from_lc(doc),
                score=float(score),
                rank=rank,
                retrieval_query="<embedding>",
            )
            for rank, (doc, score) in enumerate(rows, start=1)
        ]


_PROCESS_WIDE_FAISS: FaissVectorStore | None = None
_PROCESS_INIT_KEY: tuple[int, Path | None, bool] | None = None
_PROCESS_LOCK = threading.Lock()


def get_process_faiss_vector_store(
    *,
    embedding_dimension: int | None = None,
    persist_directory: Path | None = None,
    allow_local_index_pickles: bool = True,
) -> FaissVectorStore:
    """Return a single process-wide ``FaissVectorStore`` (one FastAPI worker)."""
    dim = embedding_dimension if embedding_dimension is not None else EMBEDDING_DIMENSIONS
    if persist_directory is None:
        persist_resolved = None
    else:
        persist_resolved = Path(persist_directory).expanduser().resolve()
    key = (dim, persist_resolved, allow_local_index_pickles)

    global _PROCESS_WIDE_FAISS, _PROCESS_INIT_KEY  # noqa: PLW0603
    with _PROCESS_LOCK:
        if _PROCESS_WIDE_FAISS is None:
            _PROCESS_WIDE_FAISS = FaissVectorStore(
                embedding_dimension=dim,
                persist_directory=persist_resolved,
                allow_local_index_pickles=allow_local_index_pickles,
            )
            _PROCESS_INIT_KEY = key
            return _PROCESS_WIDE_FAISS

        if key != _PROCESS_INIT_KEY:
            raise ValueError(
                "get_process_faiss_vector_store() already initialized with a different configuration; "
                "restart the process or keep settings stable."
            )
        return _PROCESS_WIDE_FAISS
