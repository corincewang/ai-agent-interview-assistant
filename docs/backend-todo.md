# Backend TODO（持续维护）

## 当前优先级（MVP 内）

- [ ] Planner 二次确认结果可视化：在 API 返回里明确暴露 `revised` 与 `revision_attempts_used`（当前先写入 `InterviewPlan.rubric`）。
- [ ] Planner revise 质量回归：增加一个 demo 脚本，打印 first-pass 与 revised-pass 的题目差异摘要。

## MVP 后（已记录，后续做）

- [ ] Critic 分数程序化重算（替代纯 LLM overall）
  - 为 `QuestionCritique.overall_score` 定义固定权重公式（可配置）。
  - 为 `InterviewPlanCritique.overall_score` 定义聚合公式（均值 + 覆盖惩罚项）。
  - 若 LLM 返回分数与程序重算差异过大，写入风险告警字段并落库。

- [ ] 外部爬虫与来源治理
  - 接入真实 web search/page fetch 的开关化注入。
  - 增加来源可信度白名单与域名策略（牛客/小红书/公司官网等）。
  - 将 `interview_intel_web` 的引用比例与命中质量加入评估看板。
