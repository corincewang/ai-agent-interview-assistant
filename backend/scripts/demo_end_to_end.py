import asyncio
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

from app.agents.evaluator import EvaluatorAgent
from app.agents.live_interviewer import LiveInterviewerAgent
from app.agents.report_generator import ReportGeneratorAgent
from app.config.settings import load_settings
from app.domain.models import DocumentInput, DocumentType, InterviewTurn, InterviewTurnRole
from app.graph.langgraph_workflow import LangGraphInterviewWorkflow
from app.graph.state import InterviewGraphState
from app.providers.llm import build_chat_model
from app.skills.candidate_job_matching import LLMCandidateJobMatchingSkill
from app.skills.candidate_profiling import LLMCandidateProfilingSkill
from app.skills.company_research import LLMCompanyResearchSkill
from app.skills.evaluation import LLMAnswerEvaluationSkill
from app.skills.interview_intel import LLMInterviewIntelSkill
from app.skills.interview_planning import LLMInterviewPlanningSkill
from app.skills.jd_analysis import LLMJDAnalysisSkill
from app.skills.live_interview import LLMLiveInterviewSkill
from app.skills.report_generation import LLMReportGenerationSkill
from app.skills.resume_extraction import LLMResumeExtractionSkill
from app.tools.chunking import RecursiveTextChunkingTool
from app.tools.document_parsing import LocalDocumentParsingTool
from app.tools.mock_research import MockPageFetchTool, MockWebSearchTool


async def main() -> None:
    load_dotenv()
    settings = load_settings()

    if settings.openai_api_key is None:
        print("OPENAI_API_KEY is required to run the end-to-end demo.")
        return

    llm = build_chat_model(settings)
    session_id = uuid4()
    mock_web_search_tool = MockWebSearchTool()
    mock_page_fetch_tool = MockPageFetchTool()

    preparation_workflow = LangGraphInterviewWorkflow(
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
        session_id=session_id,
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

    preparation_graph = preparation_workflow.build_preparation_graph()
    prepared_state = await preparation_graph.ainvoke(initial_state)
    interview_plan = prepared_state["interview_plan"]

    if interview_plan is None:
        print("Interview plan was not created.")
        return

    transcript: list[InterviewTurn] = []
    live_agent = LiveInterviewerAgent(
        session_id=session_id,
        plan=interview_plan,
        transcript=transcript,
        live_interview_skill=LLMLiveInterviewSkill(llm),
    )
    selected_question = await live_agent.select_next_question()
    candidate_answer = (
        "For my PartSelect AI Agent, I used Next.js with OpenAI function calling to model "
        "product search and cart actions as tools. The agent used a prompt knowledge base and "
        "structured retrieval context to avoid inventing product or transaction details. I used "
        "NDJSON streaming so the frontend could show progress as tool calls completed, which made "
        "the interaction feel more real-time. The main tradeoff was balancing fast responses with "
        "grounded retrieval and safe tool execution."
    )

    transcript.extend(
        [
            InterviewTurn(
                session_id=session_id,
                role=InterviewTurnRole.INTERVIEWER,
                content=selected_question.prompt,
                metadata={"question_id": str(selected_question.id)},
            ),
            InterviewTurn(
                session_id=session_id,
                role=InterviewTurnRole.CANDIDATE,
                content=candidate_answer,
                metadata={"question_id": str(selected_question.id)},
            ),
        ]
    )

    evaluator = EvaluatorAgent(
        session_id=session_id,
        question=selected_question,
        candidate_answer=candidate_answer,
        evaluation_skill=LLMAnswerEvaluationSkill(llm),
    )
    evaluation = await evaluator.run()

    reporter = ReportGeneratorAgent(
        session_id=session_id,
        transcript=transcript,
        evaluations=[evaluation],
        report_generation_skill=LLMReportGenerationSkill(llm),
    )
    report = await reporter.run()

    print(
        {
            "preparation": {
                "parsed_documents": len(prepared_state["parsed_documents"]),
                "document_chunks": len(prepared_state["document_chunks"]),
                "company_findings": len(prepared_state["company_sources"]),
                "interview_intel_findings": len(prepared_state["interview_intel"]),
                "question_count": len(interview_plan.questions),
            },
            "live_interview": {
                "selected_question": selected_question.prompt,
                "evaluation_scores": evaluation.scores,
                "report_preview": report[:700],
            },
        }
    )


if __name__ == "__main__":
    asyncio.run(main())

