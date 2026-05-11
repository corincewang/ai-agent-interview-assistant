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

## Why RAG Is Split Into Indexing and Retrieval

RAG has two different jobs with different latency and reliability requirements:

- Indexing: parse documents, chunk text, create embeddings, and store searchable
  chunks with metadata.
- Retrieval: take a task-specific query, search indexed chunks, rank results, and
  pass compact context into the planner or evaluator.

Keeping them separate matters because indexing is a write-time pipeline while
retrieval is a read-time pipeline. Indexing can be slower, batched, retried, and
eventually persisted in PostgreSQL with pgvector. Retrieval needs to be fast,
observable, and scoped to the current interview task.

## Why Not Put the Whole Knowledge Base in the Prompt

Putting all user notes into the prompt is simple but does not scale. It wastes
context window, increases cost, and makes the model more likely to attend to
irrelevant material. The RAG layer should retrieve only the chunks that match the
current job description, planned question, or candidate answer.

For this project, the knowledge base is useful in two places:

- Interview planning: generate questions grounded in the user's own preparation
  notes.
- Answer evaluation: check whether the candidate covered the expected concepts
  from their knowledge base.

## Why Start With Interfaces Before pgvector

The first RAG milestone should define framework-neutral contracts such as
`EmbeddingProvider`, `VectorStore`, `KnowledgeBaseIndexer`, and
`KnowledgeRetrievalTool`. This lets the product use an in-memory vector store for
tests and local demos, then swap to PostgreSQL + pgvector without rewriting
planner or evaluation logic.

This is the same design principle as the LangChain tool adapter: keep core
business contracts stable, and treat infrastructure as replaceable.

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

## RAG Interview Questions To Prepare For

**Why did you split RAG into indexing and retrieval?**

Indexing is responsible for transforming documents into searchable chunks, while
retrieval is responsible for finding the most relevant chunks for a specific task.
They have different performance profiles and failure modes, so splitting them
makes the system easier to test, retry, persist, and optimize.

**What metadata should each chunk store?**

Each chunk should store session/user ownership, document id, document type, source
file name, chunk index, text, source spans or page hints, embedding model, and
created time. For interview quality, source metadata matters because the UI and
report should eventually explain why a question was asked.

**How would you evaluate whether retrieval is good?**

I would start with qualitative traces: for each generated question or evaluation,
log the retrieval query, returned chunks, scores, and final model output. Then I
would add a small golden dataset of resume/JD/knowledge-base examples and measure
whether expected chunks appear in top-k results.

**Why not use Redis as the vector store?**

Redis is strong for cache, queues, and low-latency ephemeral state. But this
project's knowledge chunks, interview sessions, and reports are durable product
data. PostgreSQL with pgvector is a better MVP default because it keeps relational
state and vector search in one database.

**How do you avoid RAG making answers worse?**

Retrieval context should be short, source-scoped, and task-specific. The prompt
should tell the model to use retrieved context as evidence, not as absolute truth.
The system should also preserve citations and retrieval scores so poor retrieval
can be debugged instead of silently polluting generated questions.

## Risks and Tradeoffs To Mention

- Multi-agent systems can become slow and unpredictable, so the graph is explicit.
- Web interview-experience scraping has compliance risk, so MVP starts with uploaded
  and public-source information.
- Voice interaction adds latency, so text-first mock interview is the MVP path.
- Resume parsing can be noisy, especially with PDFs, so the model preserves extraction
  warnings and source spans.
- RAG can retrieve irrelevant chunks, so the system needs metadata filters,
  retrieval traces, and eventually evaluation datasets.
