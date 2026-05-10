import asyncio
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

from app.config.settings import load_settings
from app.domain.models import DocumentInput, DocumentType
from app.graph.langgraph_workflow import LangGraphInterviewWorkflow
from app.graph.state import InterviewGraphState
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
from app.tools.mock_research import MockPageFetchTool, MockWebSearchTool


async def main() -> None:
    load_dotenv()
    settings = load_settings()

    if settings.openai_api_key is None:
        print("OPENAI_API_KEY is required to run the full preparation graph demo.")
        return

    llm = build_chat_model(settings)
    mock_web_search_tool = MockWebSearchTool()
    mock_page_fetch_tool = MockPageFetchTool()

    workflow = LangGraphInterviewWorkflow(
        document_parsing_tool=LocalDocumentParsingTool(),
        chunking_tool=RecursiveTextChunkingTool(),
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
    )

    initial_state = InterviewGraphState(
        session_id=uuid4(),
        user_id=uuid4(),
        company_name="Demo AI Company",
        role_title="AI Agent Software Engineer",
        jd_text=(
            "We are looking for a software engineer to build AI agent workflows with Python, "
            "TypeScript, React, tool calling, retrieval, testing, and production-ready APIs."
        ),
        document_inputs=[
            DocumentInput(
                file_path=Path("/Users/wanghan/Desktop/王涵_简历_0506更新版.pdf"),
                document_type=DocumentType.RESUME,
            )
        ],
    )

    graph = workflow.build_preparation_graph()
    final_state = await graph.ainvoke(initial_state)

    interview_plan = final_state["interview_plan"]
    print(
        {
            "parsed_documents": len(final_state["parsed_documents"]),
            "document_chunks": len(final_state["document_chunks"]),
            "resume_profile_created": final_state["resume_profile"] is not None,
            "candidate_profile_created": final_state["candidate_profile"] is not None,
            "job_analysis_created": final_state["job_analysis"] is not None,
            "candidate_job_match_created": final_state["candidate_job_match"] is not None,
            "company_findings": len(final_state["company_sources"]),
            "interview_intel_findings": len(final_state["interview_intel"]),
            "interview_plan_created": interview_plan is not None,
            "question_count": len(interview_plan.questions) if interview_plan else 0,
        }
    )


if __name__ == "__main__":
    asyncio.run(main())

