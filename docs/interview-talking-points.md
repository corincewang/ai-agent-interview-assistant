# 面试讲解提纲

## 一句话项目介绍

我做的是一个面向技术面试准备的 AI Agent 面试助手。它可以读取候选人的简历、个人知识库、目标公司和岗位 JD，通过 LangGraph 编排多个 agent/skill，生成个性化技术面试题、追问策略和反馈报告。这个项目不是简单的 prompt wrapper，而是一个有文档解析、RAG、结构化状态、工具抽象、agent 编排和前后端 API 的完整 agentic workflow demo。

## 项目当前能力

- 上传并解析简历和知识库 PDF。
- 把简历抽取成结构化 `ResumeProfile`。
- 根据目标 JD 生成 `JobAnalysis`。
- 生成候选人和岗位的匹配分析 `CandidateJobMatch`。
- 对知识库做 RAG indexing 和 retrieval。
- 在生成面试题前检索 top-k 知识库上下文。
- 让 planner 基于简历、JD、候选人画像、公司信息、面经信息和知识库上下文生成面试计划。
- 通过 FastAPI 暴露 session、upload、prepare、turn、evaluation、report API。
- 用 Next.js 做一个最小 demo UI。

## 为什么用 LangGraph

这个系统不是线性链路，而是有多个状态阶段：

- document ingestion
- resume extraction
- candidate profiling
- JD analysis
- candidate-job matching
- knowledge-base indexing
- planning context retrieval
- company research
- interview intel
- interview planning
- live interview
- evaluation
- report generation

如果只用普通 LangChain chain，流程会变成一个很长的黑盒，很难插入新节点、debug 中间状态或重跑部分步骤。LangGraph 更适合这个项目，因为每个阶段都是显式 node，所有信息都放在 `InterviewGraphState` 里流转。这样我可以很清楚地看到：知识库是否被索引、retrieval 返回了哪些 chunks、planner 最后是否消费了这些 context。

## Tool、Skill、Agent、Graph 怎么分

- `Tool` 是确定性的底层能力，比如 PDF parsing、chunking、vector search。
- `Skill` 是一个面向任务的能力，比如 resume extraction、JD analysis、interview planning。
- `Agent` 是有角色的执行者，比如 resume extractor、candidate profiler、interview planner。
- `Graph` 是总编排层，决定这些 node 以什么顺序执行，以及每一步如何读写 state。

这个分层的目的，是避免所有逻辑都塞进一个大 prompt。Tool 可以单独测试，Skill 可以替换 prompt/model，Agent 负责绑定上下文，Graph 负责整体状态流转。

## RAG 的核心设计

我把 RAG 明确拆成两个阶段：

```text
Indexing:
ParsedDocument -> ChunkingTool -> EmbeddingProvider -> VectorStore

Retrieval:
query -> EmbeddingProvider -> VectorStore.search(top_k) -> KnowledgeRetrievalResult
```

这样拆的原因是 indexing 是写入侧，retrieval 是读取侧。Indexing 可以慢一点，可以异步、重试、批处理；retrieval 是面试规划或评价时的实时读取能力，需要快、可观察，并且能根据不同任务构造不同 query。

## RAG 相关接口

我先定义了几个 framework-neutral 的接口：

- `EmbeddingProvider`: 把 text list 转成 embedding list。
- `VectorStore`: 负责 upsert chunks 和 search top-k。
- `KnowledgeBaseIndexer`: 负责知识库 indexing pipeline。
- `KnowledgeRetrievalTool`: 负责自然语言 query 到 retrieved context 的读取 pipeline。

这样做的好处是：MVP 可以用 `InMemoryVectorStore`，后面迁移到 PostgreSQL + pgvector 时，只要实现同一个 `VectorStore` 接口，上层 graph、planner 和 evaluator 不需要重写。

## Chunking 怎么做

当前 MVP 用的是 character-based recursive chunking：

```text
chunk_size = 900 characters
chunk_overlap = 120 characters
```

它不是完全硬切，而是优先找自然边界：

```text
段落、换行、中文句号、英文句号、空格
```

这样可以尽量保证每个 chunk 语义完整。Overlap 的作用是避免概念被切断，比如前一个 chunk 讲 function calling，后一个 chunk 讲 tool schema，中间 overlap 可以让 retrieval 更稳定。

我知道字符切分不是最终最优方案。生产版本更适合升级成 hybrid chunking：

```text
先按 Markdown/section heading 切
再对太长 section 做 token-aware split
最后保留 overlap
```

但 MVP 阶段用字符窗口 + 自然边界检测，是为了先验证 RAG 闭环。

## Embedding 怎么做

Embedding 层封装成了 `OpenAIEmbeddingProvider`，默认使用：

```text
text-embedding-3-small
```

我没有直接裸调 OpenAI SDK，而是用了 LangChain LCEL：

```python
RunnableLambda(_normalize_texts)
| RunnableLambda(self._embed_normalized_texts)
```

这样后面可以继续在链上加 truncate、cache、retry、logging 或 tracing。这个 provider 对外只暴露：

```python
embed_texts(texts: list[str]) -> list[list[float]]
```

上层 indexer 和 retriever 不需要知道具体 embedding 模型来自哪里。

## 为什么 metadata 里记录 embedding model

向量相似度只有在同一个 embedding 空间里才有意义。如果今天用 `text-embedding-3-small` 生成索引，明天换成另一个模型，新旧向量不能直接混在一起搜。所以我在 MVP 里把 `embedding_model` 放进 chunk metadata，方便 debug。

后面接 PostgreSQL 时，可以把它提升成结构化字段，比如：

```text
document_chunks.embedding_model
```

或者 index-level metadata，用于模型迁移和重建索引。

## 为什么要做文本清理

真实 PDF 用 `pypdf.extract_text()` 抽取中文时，会出现很多无意义空格和断行，比如：

```text
列 表 的 流 畅 度
React
Native
```

所以我加了轻量 `_clean_extracted_text()`：

- 合并中文字符之间多余空格。
- 合并中文和中文标点之间的空格。
- 修复英文 token 和中英混排的异常断行。
- 压缩多余空行。

清理后真实知识库 PDF 从约 `27276` 字符降到约 `15550` 字符，chunk 数从 `35` 降到 `24`，retrieval preview 也明显更可读。

## RAG 怎么接进 LangGraph

我在 `InterviewGraphState` 里新增了：

```python
knowledge_indexing_result
planning_knowledge_context
```

然后在 preparation graph 里加了两个节点：

```text
ingest_documents
  -> index_knowledge_base
  -> extract_resume_profile
  -> profile_candidate
  -> analyze_jd
  -> match_candidate_to_job
  -> research_company
  -> collect_interview_intel
  -> retrieve_planning_context
  -> plan_interview
```

`index_knowledge_base` 负责把 `DocumentType.KNOWLEDGE_BASE` 的文档写入 vector store。`retrieve_planning_context` 会根据 company、role、JD、candidate profile 和 candidate-job match 构造 query，然后 retrieve top-k 知识库 chunks，交给 planner。

## Planner 怎么使用 RAG

Planner 的 contract 现在接收：

```python
knowledge_context: KnowledgeRetrievalResult | None
```

Prompt 里会把 retrieved context 格式化成：

```text
Rank
Score
Chunk index
Excerpt
```

并明确要求：如果 retrieved knowledge context 存在，至少两个问题要显式围绕知识库里的主题生成，同时不能说候选人在某个 topic 上经验有限，如果 retrieved context 已经包含这个 topic 的项目细节。

## 真实知识库 demo 结果

我用真实文件 `/Users/wanghan/Desktop/简历+前端问题.pdf` 跑过 RAG demo：

```text
page_count: 16
indexed_chunks: 24
warnings: []
```

检索结果可以命中：

- React / Redux / Zustand / re-render / React.memo / selector
- FlatList / keyExtractor / rendering performance
- AI Agent / function calling / tool design
- streaming / NDJSON / Vercel buffering / Cache-Control
- grounding / hallucination control / single-agent multi-tool design

我也跑了完整 preparation graph with RAG：

```text
parsed_documents: 2
indexed_chunks: 24
retrieved_planning_chunks: 5
question_count: 6
```

这说明 RAG 不只是一个单独 demo，而是已经进入主 agent workflow，并且 planner 可以消费 retrieved context 来生成面试问题。

## 当前 RAG 的不足和下一步

当前 retrieval 是纯 embedding 相似度，所以有时候 query 里有 `performance`，可能会把 streaming performance 和 React rendering performance 混在一起。下一步可以做：

- query rewrite：把 JD + candidate profile 转成更精准的 retrieval query。
- hybrid retrieval：embedding + keyword filter。
- reranking：对 top-k 做二次排序。
- token-aware / section-aware chunking。
- PostgreSQL + pgvector 持久化。
- retrieval evaluation golden set。

## 简历里可以怎么写

```text
Built a RAG-enhanced multi-agent technical interview assistant using FastAPI, LangGraph, LangChain LCEL, OpenAI, and Next.js. Designed separate indexing and retrieval pipelines for user-provided knowledge-base documents, integrated top-k retrieved context into interview planning, and validated the workflow on real resume/interview-prep PDFs.
```

中文版可以讲：

```text
我实现了一个带 RAG 的多 Agent 技术面试助手。系统会解析简历和知识库 PDF，对知识库进行 chunking、embedding 和向量检索，在面试规划前检索 top-k 相关上下文，并让 planner 基于简历、JD、岗位匹配和用户自己的准备材料生成更个性化的技术面试题。
```

## 面试中可以主动强调的 tradeoff

- MVP 用 in-memory vector store，是为了先验证 RAG 闭环；生产会迁移到 PostgreSQL + pgvector。
- MVP 用字符切分，是为了兼容 PDF/TXT/MD；生产会升级为 section-aware + token-aware hybrid chunking。
- MVP 用纯 embedding retrieval，下一步会加 query rewrite、keyword filter 和 rerank。
- RAG context 只作为 evidence，不应该让模型把检索结果当成绝对真理。
- graph 显式拆 node，是为了让每一步可 debug、可替换、可观测。
