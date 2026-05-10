import asyncio
from uuid import uuid4

from dotenv import load_dotenv

from app.agents.evaluator import EvaluatorAgent
from app.agents.live_interviewer import LiveInterviewerAgent
from app.agents.report_generator import ReportGeneratorAgent
from app.config.settings import load_settings
from app.domain.models import (
    InterviewMode,
    InterviewPlan,
    InterviewQuestion,
    InterviewTurn,
    InterviewTurnRole,
)
from app.providers.llm import build_chat_model
from app.skills.evaluation import LLMAnswerEvaluationSkill
from app.skills.live_interview import LLMLiveInterviewSkill
from app.skills.report_generation import LLMReportGenerationSkill


async def main() -> None:
    load_dotenv()
    settings = load_settings()

    if settings.openai_api_key is None:
        print("OPENAI_API_KEY is required to run the live interview demo.")
        return

    llm = build_chat_model(settings)
    session_id = uuid4()
    question = InterviewQuestion(
        id=uuid4(),
        prompt=(
            "Walk me through the architecture of your PartSelect AI Agent project. "
            "How did you design tool calling, retrieval, and streaming?"
        ),
        topic="AI agent architecture",
        difficulty="medium",
        expected_signals=[
            "tool schema design",
            "retrieval grounding",
            "streaming implementation",
            "failure handling",
        ],
        follow_up_strategy=[
            "Probe tradeoffs",
            "Ask for implementation details",
            "Check hallucination mitigation",
        ],
    )
    plan = InterviewPlan(
        session_id=session_id,
        mode=InterviewMode.AI_AGENT,
        questions=[question],
        rubric={
            "correctness": "Technical explanation is accurate.",
            "depth": "Answer includes implementation details and tradeoffs.",
            "communication": "Answer is structured and easy to follow.",
        },
        candidate_storyline="AI agent engineer with frontend and full-stack project experience.",
        planned_deep_dives=["PartSelect AI Agent", "tool calling", "streaming"],
    )
    transcript: list[InterviewTurn] = []
    candidate_answer = (
        "I built the PartSelect AI Agent with Next.js and OpenAI function calling. "
        "The agent used structured tools for product search and cart actions, and I added "
        "NDJSON streaming so the UI could receive incremental updates. I also used a prompt "
        "knowledge base to keep product and transaction facts grounded instead of letting the "
        "model invent them."
    )

    live_agent = LiveInterviewerAgent(
        session_id=session_id,
        plan=plan,
        transcript=transcript,
        live_interview_skill=LLMLiveInterviewSkill(llm),
    )
    selected_question = await live_agent.select_next_question()
    follow_up = await live_agent.decide_follow_up(
        current_question=selected_question,
        candidate_answer=candidate_answer,
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
            "selected_question": selected_question.prompt,
            "follow_up": follow_up.prompt if follow_up else None,
            "evaluation_scores": evaluation.scores,
            "report_preview": report[:500],
        }
    )


if __name__ == "__main__":
    asyncio.run(main())

