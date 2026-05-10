from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from app.config.settings import Settings


def build_chat_model(settings: Settings) -> BaseChatModel:
    if settings.openai_api_key is None:
        raise ValueError("OPENAI_API_KEY is required to build the default chat model")

    return ChatOpenAI(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )

