# Backend TODO（持续维护）

## 已完成（从待办移出）

- [x] 文档解析主路径统一为 `unstructured.partition.auto`（PDF/DOCX）。
- [x] OCR fallback 路径接通（非文本可提取场景可降级）。
- [x] 文本清洗基础能力已上线（段落断裂与异常空白初步处理）。
- [x] 分块升级到“结构优先 + 递归切分”主路径（不再按页码硬切）。
- [x] 检索 rerank 已接入（FlashRank），召回结果支持重排后再返回。

## P0（当前主线，优先做）

- [ ] Planner 质量闭环补齐（生成 -> 质检 -> 修订 -> 记录）
  - [ ] 将 `planner_revision_attempts`、`revised`、`revision_attempts_used` 作为稳定 API 字段返回（不只在内部 metadata/rubric）。
  - [ ] 记录 first-pass 与 revised-pass 的差异摘要（新增调试/演示脚本）。
  - [ ] 将每次 revise 的触发原因（低分维度、失败字段）结构化落库，便于回放。

- [ ] 面试题生成质量提升（12 题三类配额）
  - [ ] 强约束三类题目配额：`project_deep_dive` / `tech_deep_dive` / `scenario` 各 4 题。
  - [ ] 失败兜底策略：按类别自动补题，避免 `expected 4, got 3` 反复重试。
  - [ ] 输出稳定化：统一 question_type/source_scope/source_id 的完整性校验。

- [ ] RAG 查询与召回优化（面向“出题质量”，不是纯相似度）
  - [ ] 多 query 规划：按三类题分别构造 retrieval query。
  - [ ] hybrid retrieval：向量 + 关键词/metadata filter（role、topic、source_type）。
  - [ ] 去重策略：chunk 级 + 语义近重复去重，避免上下文同质化。

- [ ] 检索复用能力（同岗位跨简历复用）
  - [ ] 设计“岗位画像缓存层”：按 `company + role + jd_hash` 缓存 JD 分析/岗位能力框架。
  - [ ] 新简历进入时只重算候选人侧（resume/profile/match），复用岗位侧中间结果。
  - [ ] 为复用命中率增加埋点（cache_hit/cache_miss）和时延收益统计。

- [ ] Chunk 粒度从“字符近似”升级为“token 可控”
  - [ ] 在切分阶段增加 tokenizer 计数器，支持 `max_chunk_tokens` 与 `chunk_token_overlap`。
  - [ ] 保留语义边界优先，超阈值时再递归二次切分。
  - [ ] 在 metadata 中记录 `chunk_tokens`，便于后续召回质量分析。

- [ ] 可观测性最小闭环（LangSmith）
  - [ ] 固化 `resume -> prepare -> questions` 全链路 trace 命名与 tags 规范。
  - [ ] 关键 span 打点：parse/chunk/retrieve/rerank/plan/critic/revise。
  - [ ] 在 trace metadata 中补充核心指标：retrieval query、top-k、命中文档、耗时、失败原因。

## P1（MVP 完成后立刻跟进）

- [ ] Critic 分数程序化重算（替代纯 LLM overall）
  - [ ] 为 `QuestionCritique.overall_score` 定义固定权重公式（可配置）。
  - [ ] 为 `InterviewPlanCritique.overall_score` 定义聚合公式（均值 + 覆盖惩罚项）。
  - [ ] 若 LLM 分数与程序重算偏差过大，写入风险告警字段并落库。

- [ ] RAG 数据处理增强
  - [ ] 文本清洗标准化 2.0（标点粘连修复、问答结构保护、标题去重）。
  - [ ] 大文件流式 ingestion（分页解析 -> 分批 chunk/index），支持“先学先用”。
  - [ ] 解析质量回归集（固定 PDF/DOCX 样本 + 指标对比）。

- [ ] 评估体系
  - [ ] 构建离线评测集（简历/JD/知识库/期望题目）。
  - [ ] 评估指标：JD 覆盖、简历贴合、RAG grounding、问题具体性、追问潜力。
  - [ ] 将 `rag_usage_score` 与证据引用率解耦统计，避免“有引用但得 0 分”不可解释。

## P2（MVP 后扩展项）

- [ ] 外部爬虫与来源治理
  - [ ] 接入真实 web search/page fetch 的开关化注入。
  - [ ] 增加来源可信度白名单与域名策略（牛客/小红书/公司官网等）。
  - [ ] 新增 source_scope/source_type：`interview_intel_web`（面经来源单独可追踪）。
  - [ ] 将外部来源命中率、引用率、风险备注纳入看板。

- [ ] 后端模块化重构（降低耦合）
  - [ ] 将 `langgraph_workflow.py` 中 planning retrieval/query merge/observability 拆分到独立模块。
  - [ ] 保持 graph 只做编排，业务逻辑下沉到 service/skill/tool 层。
  - [ ] 为拆分模块补单测（输入 state -> 输出 state）避免回归。

- [ ] 生产化工程项
  - [ ] 任务队列化（重解析与重索引异步化、可重试、可取消）。
  - [ ] 资源隔离（CPU 密集解析与 API 服务解耦）。
  - [ ] 失败恢复（断点续跑、部分成功可见、幂等重放）。
