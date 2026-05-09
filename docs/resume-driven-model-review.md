# Resume-Driven Model Review

This review uses the first real user profile: Wang Han, a CMU student targeting
frontend, mobile, full-stack, and AI agent engineering roles.

## Resume Signals Observed

- Education: Carnegie Mellon University, computer science and information systems,
HCI minor, game design minor, expected graduation May 2026.
- Skills: Java, Python, Swift, JavaScript, TypeScript, React, React Native, Node.js,
Next.js, Tailwind, AWS, Vercel, Git, CI/CD, AI Agent development, MySQL.
- Internship experience:
  - Menu Inc.: React Native, Redux, Firebase Analytics, Cursor AI, MCP, Detox E2E.
  - Toyz Electronics Inc.: React.js, Node.js, Azure App Service, Azure DevOps,
  Microsoft PlayFab, Azure AI chatbot.
- Project experience:
  - PartSelect AI Agent: Next.js, OpenAI Function Calling, task-oriented agent,
  prompt knowledge base, NDJSON streaming, ecommerce retrieval and checkout flow.
  - Pawse iOS App: Swift, SwiftUI, social feed, image cache, AWS Lambda, Firebase,
  S3, TestFlight, Fastlane.
  - Santorini Java game: Java, Maven, RESTful API, OOP, AWS deployment, CloudWatch.

## Model Issues Found

- `CandidateProfile` was too flat for a resume with internships, projects, metrics,
technical stacks, links, and language abilities.
- `DocumentParsingTool` returned only raw text, which loses page-level evidence and
makes later feedback reports harder to cite.
- The graph jumped from document ingestion directly to candidate profiling, but a
real resume needs an explicit resume extraction step first.
- Quantified claims such as "14%", "8%", "3x", "3,700+", and "15%" should be modeled
as first-class facts because they are high-value interview follow-up targets.
- AI agent projects need architecture notes, tool-calling details, streaming details,
and guardrail/prompt-knowledge-base details, not just a generic project summary.

## Contract Changes Made

- Added `ParsedDocument` and `SourceSpan` to preserve document evidence.
- Added `ResumeProfile` as a structured resume fact model.
- Added normalized resume submodels:
  - `EducationItem`
  - `SkillInventory`
  - `LanguageProficiency`
  - `WorkExperience`
  - `ProjectExperience`
  - `QuantifiedImpact`
- Updated `CandidateProfile` to include `resume_profile`, `strongest_signals`,
and `interview_positioning`.
- Updated `InterviewPlan` to include `candidate_storyline` and `planned_deep_dives`.
- Updated tool contracts so document parsing returns `ParsedDocument`.
- Added `ResumeExtractionSkill` and `ResumeExtractorAgent`.
- Added `extract_resume_profile` to the graph workflow.

## Resulting Flow

```text
ParsedDocument
  -> ResumeProfile
  -> CandidateProfile
  -> JobAnalysis
  -> InterviewPlan
  -> LiveInterview
  -> EvaluationReport
```

This keeps resume facts separate from interview strategy. That matters because the
same resume can produce different candidate profiles for different roles, such as
frontend, mobile, backend, or AI agent engineer.