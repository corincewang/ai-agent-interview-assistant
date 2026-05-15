import asyncio
from pathlib import Path
from uuid import uuid4

from app.config.settings import load_settings
from app.domain.models import DocumentInput, DocumentType
from app.graph.langgraph_workflow import LangGraphInterviewWorkflow
from app.graph.state import InterviewGraphState
from app.providers.embeddings import OpenAIEmbeddingProvider
from app.providers.llm import build_chat_model
from app.skills.candidate_job_matching import LLMCandidateJobMatchingSkill
from app.skills.candidate_profiling import LLMCandidateProfilingSkill
from app.skills.company_research import LLMCompanyResearchSkill
from app.skills.interview_intel import LLMInterviewIntelSkill
from app.skills.interview_planning import LLMInterviewPlanningSkill
from app.skills.jd_analysis import LLMJDAnalysisSkill
from app.skills.resume_extraction import LLMResumeExtractionSkill
from app.tools.chunking import RecursiveTextChunkingTool
from app.tools.document_parsing import LocalDocumentParsingTool
from app.tools.faiss_vector_store import FaissVectorStore
from app.tools.knowledge_retrieval import DefaultKnowledgeRetrievalTool
from app.tools.mock_research import MockPageFetchTool, MockWebSearchTool
from app.tools.windowed_knowledge_indexer import WindowedKnowledgeBaseIndexer


RESUME_PATH = Path("/Users/wanghan/Desktop/王涵_简历_0506更新版.pdf")
KNOWLEDGE_BASE_PATH = Path("/Users/wanghan/Desktop/简历+前端问题.pdf")


async def main() -> None:
    settings = load_settings()
    if settings.openai_api_key is None:
        print("OPENAI_API_KEY is required to run the RAG preparation graph demo.")
        return

    llm = build_chat_model(settings)
    embedding_provider = OpenAIEmbeddingProvider(api_key=settings.openai_api_key)
    vector_store = FaissVectorStore()
    chunker = RecursiveTextChunkingTool(chunk_size=900, chunk_overlap=120)
    mock_web_search_tool = MockWebSearchTool()
    mock_page_fetch_tool = MockPageFetchTool()
    document_parser = LocalDocumentParsingTool()

    workflow = LangGraphInterviewWorkflow(
        document_parsing_tool=document_parser,
        chunking_tool=chunker,
        resume_extraction_skill=LLMResumeExtractionSkill(llm),
        candidate_profiling_skill=LLMCandidateProfilingSkill(llm),
        jd_analysis_skill=LLMJDAnalysisSkill(llm),
        candidate_job_matching_skill=LLMCandidateJobMatchingSkill(llm),
        company_research_skill=LLMCompanyResearchSkill(
            llm=llm,
            web_search_tool=mock_web_search_tool,
            page_fetch_tool=mock_page_fetch_tool,
        ),
        interview_intel_skill=LLMInterviewIntelSkill(
            llm=llm,
            web_search_tool=mock_web_search_tool,
            page_fetch_tool=mock_page_fetch_tool,
        ),
        interview_planning_skill=LLMInterviewPlanningSkill(llm),
        knowledge_base_indexer=WindowedKnowledgeBaseIndexer(
            document_parser=document_parser,
            chunking_tool=chunker,
            embedding_provider=embedding_provider,
            vector_store=vector_store,
        ),
        knowledge_retrieval_tool=DefaultKnowledgeRetrievalTool(
            embedding_provider=embedding_provider,
            vector_store=vector_store,
        ),
    )

    initial_state = InterviewGraphState(
        session_id=uuid4(),
        user_id=uuid4(),
        company_name="Demo Frontend AI Company",
        role_title="Frontend / AI Agent Software Engineer",
        target_track="Frontend Performance / AI Product UI",
        jd_text=(
            "Build production frontend experiences for AI agent products using React, "
            "TypeScript, streaming APIs, tool calling, retrieval, performance profiling, "
            "testing, and product-minded UX judgment."
        ),
        document_inputs=[
            DocumentInput(file_path=RESUME_PATH, document_type=DocumentType.RESUME),
            DocumentInput(
                file_path=KNOWLEDGE_BASE_PATH,
                document_type=DocumentType.KNOWLEDGE_BASE,
            ),
        ],
    )

    preparation_graph = workflow.build_preparation_graph()
    prepared_state = await preparation_graph.ainvoke(initial_state)

    indexing_result = prepared_state["knowledge_indexing_result"]
    planning_context = prepared_state["planning_knowledge_context"]
    interview_plan = prepared_state["interview_plan"]

    print(
        {
            "parsed_documents": len(prepared_state["parsed_documents"]),
            "indexed_chunks": (
                len(indexing_result.indexed_chunk_ids)
                if indexing_result is not None
                else 0
            ),
            "retrieved_planning_chunks": (
                len(planning_context.chunks)
                if planning_context is not None
                else 0
            ),
            "question_count": len(interview_plan.questions) if interview_plan else 0,
        }
    )

    if planning_context is not None:
        print("\nRetrieved planning context:")
        for chunk in planning_context.chunks:
            preview = " ".join(chunk.chunk.text.split())[:420]
            print(
                {
                    "rank": chunk.rank,
                    "score": round(chunk.score, 4),
                    "chunk_index": chunk.chunk.metadata.get("chunk_index"),
                    "preview": preview,
                }
            )

    if interview_plan is not None:
        print("\nGenerated interview questions:")
        for index, question in enumerate(interview_plan.questions, start=1):
            print(
                {
                    "number": index,
                    "topic": question.topic,
                    "difficulty": question.difficulty,
                    "prompt": question.prompt,
                    "expected_signals": question.expected_signals,
                }
            )


if __name__ == "__main__":
    asyncio.run(main())
