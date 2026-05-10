from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    openai_model: str
    enable_external_research: bool


def load_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        enable_external_research=_read_bool("ENABLE_EXTERNAL_RESEARCH", default=False),
    )


def _read_bool(name: str, default: bool) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    return raw_value.strip().lower() in {"1", "true", "yes", "on"}

