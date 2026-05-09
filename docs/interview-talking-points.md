# Interview Talking Points

## One-Sentence Project Pitch

I built an agentic technical interview assistant that uses a candidate's resume,
knowledge base, job description, and company research to generate personalized
mock interviews, adaptive follow-ups, and evidence-grounded feedback.

## Why LangGraph Instead of a Simple Chain

The workflow has multiple stateful phases:

- document ingestion
- resume extraction
- candidate profiling
- JD analysis
- company research
- interview planning
- live interview turns
- answer evaluation
- final report generation

A simple chain is linear and hard to pause, retry, inspect, or branch. LangGraph
lets the system model each phase as a node with explicit state transitions. This
makes the agent workflow easier to test, debug, and extend.

## Why Tools, Skills, Agents, and Graph Are Separate

- Tool: a small deterministic capability, such as parsing a PDF or chunking text.
- Skill: a higher-level capability that combines tools, prompts, and output schemas.
- Agent: a role with a goal, such as candidate profiler or live interviewer.
- Graph: the workflow controller that decides the order in which agents and skills run.

This separation avoids a common agent-system failure mode where prompts, retrieval,
business logic, and persistence become tangled together.

## Why Source Spans Matter

The assistant should not invent resume facts. `ParsedDocument` stores raw text plus
`SourceSpan` evidence so later stages can trace candidate claims back to the source
resume, JD, or knowledge base.

This supports:

- grounded follow-up questions
- explainable feedback reports
- debugging extraction errors
- future UI citations

## Why Preparation and Live Interview Are Separate Graphs

The preparation graph can be slower because it does heavy work: parsing, retrieval,
research, and planning. The live interview graph must be fast because the user is
waiting for the next question.

This creates a practical latency boundary:

```text
Preparation: heavy, asynchronous, research-oriented
Live interview: lightweight, stateful, low-latency
```

## Resume-Specific Deep Dive Topics

For Wang Han's resume, the strongest technical interview angles are:

- AI agent architecture in the PartSelect project
- OpenAI function calling and task orchestration
- HTTP chunked streaming with NDJSON
- RAG and prompt knowledge-base design
- React Native performance and Redux state management
- Detox E2E testing strategy
- SwiftUI architecture, image caching, and AWS Lambda integration
- CI/CD experience with Azure DevOps, Fastlane, and cloud deployments

## Risks and Tradeoffs To Mention

- Multi-agent systems can become slow and unpredictable, so the graph is explicit.
- Web interview-experience scraping has compliance risk, so MVP starts with uploaded
  and public-source information.
- Voice interaction adds latency, so text-first mock interview is the MVP path.
- Resume parsing can be noisy, especially with PDFs, so the model preserves extraction
  warnings and source spans.

