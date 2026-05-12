from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    openai_model: str
    enable_external_research: bool
    database_url: str | None
    # postgres | faiss | memory — see _resolve_vector_store_backend when unset.
    vector_store_backend: str
    #: When set (e.g. ``FAISS_PERSIST_DIRECTORY=/data/faiss``), each session's index is saved under
    # ``<resolved>/<session_id>/index.{faiss,pkl}`` (LangChain layout).
    faiss_persist_directory: Path | None
    #: Only load ``*.pkl`` docstores produced by this app (pickle deserialization risk).
    faiss_allow_local_index_pickles: bool


def load_settings() -> Settings:
    load_dotenv()

    database_url = os.getenv("DATABASE_URL")
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        enable_external_research=_read_bool("ENABLE_EXTERNAL_RESEARCH", default=False),
        database_url=database_url,
        vector_store_backend=_resolve_vector_store_backend(
            raw=os.getenv("VECTOR_STORE_BACKEND", ""),
            database_url=database_url,
        ),
        faiss_persist_directory=_optional_path(os.getenv("FAISS_PERSIST_DIRECTORY")),
        faiss_allow_local_index_pickles=_read_bool(
            "FAISS_ALLOW_LOCAL_INDEX_PICKLES",
            default=True,
        ),
    )


def _read_bool(name: str, default: bool) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


def _optional_path(raw: str | None) -> Path | None:
    if raw is None:
        return None
    trimmed = raw.strip()
    if not trimmed:
        return None
    return Path(trimmed).expanduser().resolve()


def _resolve_vector_store_backend(raw: str, database_url: str | None) -> str:
    trimmed = raw.strip().lower()
    if trimmed in {"postgres", "faiss", "memory"}:
        return trimmed
    if database_url:
        return "postgres"
    return "faiss"
