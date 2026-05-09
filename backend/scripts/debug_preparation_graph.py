import asyncio
from pathlib import Path
from uuid import uuid4

from app.domain.models import DocumentInput, DocumentType, InterviewMode
from app.graph.langgraph_workflow import LangGraphInterviewWorkflow
from app.graph.state import InterviewGraphState
from app.tools.chunking import RecursiveTextChunkingTool
from app.tools.document_parsing import LocalDocumentParsingTool


async def main() -> None:
    resume_path = Path("/Users/wanghan/Desktop/王涵_简历_0506更新版.pdf")
    workflow = LangGraphInterviewWorkflow(
        document_parsing_tool=LocalDocumentParsingTool(),
        chunking_tool=RecursiveTextChunkingTool(),
    )

    graph = workflow.build_preparation_graph()
    initial_state = InterviewGraphState(
        session_id=uuid4(),
        user_id=uuid4(),
        company_name="Demo Company",
        role_title="Software Engineer",
        jd_text="Build agentic software systems with Python, TypeScript, and modern web frameworks.",
        document_inputs=[
            DocumentInput(
                file_path=resume_path,
                document_type=DocumentType.RESUME,
            )
        ],
    )

    final_state = await graph.ainvoke(initial_state)
    print(
        {
            "mode": InterviewMode.GENERAL_SWE.value,
            "parsed_documents": len(final_state["parsed_documents"]),
            "document_chunks": len(final_state["document_chunks"]),
            "resume_profile_created": final_state["resume_profile"] is not None,
            "candidate_profile_created": final_state["candidate_profile"] is not None,
            "interview_plan_created": final_state["interview_plan"] is not None,
        }
    )


if __name__ == "__main__":
    asyncio.run(main())

