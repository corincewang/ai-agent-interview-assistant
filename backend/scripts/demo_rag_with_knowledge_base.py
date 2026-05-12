import asyncio
from dataclasses import replace
from pathlib import Path
from uuid import uuid4

from app.config.settings import load_settings
from app.domain.models import DocumentType
from app.providers.embeddings import OpenAIEmbeddingProvider
from app.tools.chunking import RecursiveTextChunkingTool
from app.tools.document_parsing import LocalDocumentParsingTool
from app.tools.faiss_vector_store import FaissVectorStore
from app.tools.knowledge_retrieval import DefaultKnowledgeRetrievalTool
from app.tools.windowed_knowledge_indexer import WindowedKnowledgeBaseIndexer


KNOWLEDGE_BASE_PATH = Path("/Users/wanghan/Desktop/简历+前端问题.pdf")


async def main() -> None:
    settings = load_settings()
    if settings.openai_api_key is None:
        print("OPENAI_API_KEY is required to run the RAG demo.")
        return

    session_id = uuid4()
    parser = LocalDocumentParsingTool()
    chunker = RecursiveTextChunkingTool(chunk_size=900, chunk_overlap=120)
    embedding_provider = OpenAIEmbeddingProvider(api_key=settings.openai_api_key)
    vector_store = FaissVectorStore()
    indexer = WindowedKnowledgeBaseIndexer(
        document_parser=parser,
        chunking_tool=chunker,
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )
    retriever = DefaultKnowledgeRetrievalTool(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    document = await parser.parse_document(
        file_path=KNOWLEDGE_BASE_PATH,
        document_type=DocumentType.KNOWLEDGE_BASE,
    )
    document_with_path = replace(
        document,
        metadata={
            **document.metadata,
            "source_file_path": str(KNOWLEDGE_BASE_PATH.resolve()),
        },
    )
    indexing_result = await indexer.index_documents(
        session_id=session_id,
        documents=[document_with_path],
    )

    queries = [
        "frontend interview questions about React state management and rendering",
        "AI agent project function calling streaming and tool design",
        "JavaScript TypeScript frontend performance interview preparation",
    ]

    print(
        {
            "session_id": str(session_id),
            "file_name": document.metadata.get("file_name"),
            "page_count": document.metadata.get("page_count"),
            "raw_text_chars": len(document.raw_text),
            "indexed_chunks": len(indexing_result.indexed_chunk_ids),
            "warnings": indexing_result.warnings,
        }
    )

    for query in queries:
        retrieval_result = await retriever.retrieve_knowledge(
            session_id=session_id,
            query=query,
            top_k=3,
            document_types=[DocumentType.KNOWLEDGE_BASE],
        )
        print(f"\nQUERY: {query}")
        for result in retrieval_result.chunks:
            metadata = result.chunk.metadata
            preview = " ".join(result.chunk.text.split())[:500]
            print(
                {
                    "rank": result.rank,
                    "score": round(result.score, 4),
                    "chunk_index": metadata.get("chunk_index"),
                    "start_char": metadata.get("start_char"),
                    "end_char": metadata.get("end_char"),
                    "preview": preview,
                }
            )


if __name__ == "__main__":
    asyncio.run(main())
