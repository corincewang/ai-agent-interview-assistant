from collections.abc import Sequence

from langchain_core.runnables import RunnableLambda
from langchain_openai import OpenAIEmbeddings


class OpenAIEmbeddingProvider:
    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
    ) -> None:
        self.model = model
        self._embeddings = OpenAIEmbeddings(
            api_key=api_key,
            model=model,
        )

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        chain = (
            RunnableLambda(_normalize_texts)
            | RunnableLambda(self._embed_normalized_texts)
        )
        return await chain.ainvoke(texts)

    async def _embed_normalized_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        return await self._embeddings.aembed_documents(texts)


def _normalize_texts(texts: Sequence[str]) -> list[str]:
    return [text.strip() for text in texts if text.strip()]
