import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app.domain.models import DocumentType, SourceCitation


class SerperWebSearchTool:
    """Use Serper.dev to get web search results for company/interview intel retrieval."""

    def __init__(
        self,
        api_key: str | None = None,
        endpoint: str = "https://google.serper.dev/search",
        timeout_seconds: int = 20,
    ) -> None:
        self.api_key = api_key or os.getenv("SERPER_API_KEY", "")
        self.endpoint = endpoint
        self.timeout_seconds = timeout_seconds

    async def search_web(self, query: str, limit: int) -> list[SourceCitation]:
        if not self.api_key.strip():
            return []

        payload = json.dumps({"q": query, "num": max(1, limit)})
        request = Request(
            self.endpoint,
            data=payload.encode("utf-8"),
            method="POST",
            headers={
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json",
            },
        )
        with urlopen(request, timeout=self.timeout_seconds) as response:
            body = response.read().decode("utf-8")
        parsed = json.loads(body)

        organic = parsed.get("organic", [])
        citations: list[SourceCitation] = []
        for item in organic[:limit]:
            title = str(item.get("title", "")).strip()
            url = str(item.get("link", "")).strip()
            if not title:
                continue
            citations.append(
                SourceCitation(
                    title=title,
                    url=url or None,
                    source_type=DocumentType.INTERVIEW_INTEL,
                    confidence=0.6,
                )
            )
        return citations


class HttpPageFetchTool:
    """Fetch public page text via a basic HTTP GET request."""

    def __init__(self, timeout_seconds: int = 20) -> None:
        self.timeout_seconds = timeout_seconds

    async def fetch_public_page(self, url: str) -> str:
        if not url.strip():
            return ""
        request = Request(
            url,
            method="GET",
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; InterviewAssistantBot/1.0)",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        )
        with urlopen(request, timeout=self.timeout_seconds) as response:
            body = response.read()
        return body.decode("utf-8", errors="ignore")

