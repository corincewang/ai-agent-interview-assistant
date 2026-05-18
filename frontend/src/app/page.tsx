"use client";

import {
  Brain,
  CheckCircle2,
  CircleAlert,
  FileText,
  Loader2,
  MessageSquareText,
  Play,
  Send,
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import {
  checkHealth,
  createInterviewSession,
  evaluateSession,
  generateReport,
  prepareInterviewSessionStream,
  submitAnswer,
  uploadDocument,
} from "@/lib/api/client";
import { InterviewPlanView, InterviewQuestionView } from "@/lib/api/contracts";

type Tab = "plan" | "interview" | "report";

const defaultJd =
  "Build AI agent workflows with Python, TypeScript, React, tool calling, retrieval, testing, and production-ready APIs.";

export default function HomePage() {
  const [companyName, setCompanyName] = useState("Demo AI Company");
  const [roleTitle, setRoleTitle] = useState("AI Agent Software Engineer");
  const [jobDescription, setJobDescription] = useState(defaultJd);
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [knowledgeFiles, setKnowledgeFiles] = useState<File[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [plan, setPlan] = useState<InterviewPlanView | null>(null);
  const [selectedQuestionId, setSelectedQuestionId] = useState<string | null>(null);
  const [answerDrafts, setAnswerDrafts] = useState<Record<string, string>>({});
  const [submittedAnswers, setSubmittedAnswers] = useState<Record<string, string>>({});
  const [followUp, setFollowUp] = useState<InterviewQuestionView | null>(null);
  const [report, setReport] = useState("");
  const [activeTab, setActiveTab] = useState<Tab>("plan");
  const [busyLabel, setBusyLabel] = useState<string | null>(null);
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void checkHealth().then(setBackendOnline);
  }, []);

  const selectedQuestion = useMemo(() => {
    if (!plan) return null;
    return (
      plan.questions.find((question) => question.id === selectedQuestionId) ??
      plan.questions[0] ??
      null
    );
  }, [plan, selectedQuestionId]);

  const statusText = useMemo(() => {
    if (busyLabel) return busyLabel;
    if (sessionId) return "Session ready";
    if (backendOnline === null) return "Checking backend";
    return backendOnline ? "Backend online" : "Backend unavailable";
  }, [backendOnline, busyLabel, sessionId]);

  async function runSetup() {
    if (!resumeFile) {
      setError("请先上传简历文件（必填）。");
      return;
    }

    setError(null);
    setBusyLabel("Creating session");

    try {
      const session = await createInterviewSession({
        company_name: companyName,
        role_title: roleTitle,
        target_track: roleTitle,
        jd_text: jobDescription,
      });
      setSessionId(session.session_id);

      setBusyLabel("Uploading resume");
      await uploadDocument(session.session_id, "resume", resumeFile);

      if (knowledgeFiles.length > 0) {
        setBusyLabel("Uploading knowledge files");
      }
      for (const file of knowledgeFiles) {
        await uploadDocument(session.session_id, "knowledge_base", file);
      }

      setBusyLabel("Preparing interview plan");
      setActiveTab("interview");
      setPlan(null);
      setSelectedQuestionId(null);
      setAnswerDrafts({});
      setSubmittedAnswers({});
      setFollowUp(null);

      await prepareInterviewSessionStream(session.session_id, (event) => {
        if (event.event === "progress") {
          setBusyLabel(event.message);
          return;
        }

        if (event.event === "plan") {
          setBusyLabel("Streaming interview questions");
          setPlan({
            session_id: event.session_id,
            mode: "general_swe",
            questions: [],
            rubric: {},
            candidate_storyline: event.candidate_storyline,
            planned_deep_dives: event.planned_deep_dives,
          });
          return;
        }

        if (event.event === "question") {
          setPlan((currentPlan) => {
            if (!currentPlan) {
              return {
                session_id: session.session_id,
                mode: "general_swe",
                questions: [event.question],
                rubric: {},
                candidate_storyline: "",
                planned_deep_dives: [],
              };
            }
            if (event.index === 1) {
              return {
                ...currentPlan,
                questions: [event.question],
              };
            }
            return {
              ...currentPlan,
              questions: [...currentPlan.questions, event.question],
            };
          });
          setSelectedQuestionId((current) =>
            event.index === 1 ? event.question.id : current ?? event.question.id,
          );
          return;
        }

        if (event.event === "complete") {
          setPlan(event.interview_plan);
          setSelectedQuestionId(
            (current) => current ?? event.interview_plan.questions[0]?.id ?? null,
          );
          return;
        }

        if (event.event === "error") {
          throw new Error(event.message);
        }
      });
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Setup failed");
    } finally {
      setBusyLabel(null);
    }
  }

  async function submitCurrentAnswer() {
    if (!sessionId || !selectedQuestion) return;
    const currentAnswer = answerDrafts[selectedQuestion.id] ?? "";

    setError(null);
    setBusyLabel("Submitting answer");

    try {
      const result = await submitAnswer(sessionId, {
        question_id: selectedQuestion.id,
        answer: currentAnswer,
      });
      setSubmittedAnswers((current) => ({
        ...current,
        [selectedQuestion.id]: currentAnswer,
      }));
      setAnswerDrafts((current) => ({
        ...current,
        [selectedQuestion.id]: "",
      }));
      setFollowUp(result.follow_up_question);
      if (!result.follow_up_question && plan) {
        const currentIndex = plan.questions.findIndex(
          (question) => question.id === selectedQuestion.id,
        );
        const nextQuestion = plan.questions
          .slice(currentIndex + 1)
          .find((question) => !submittedAnswers[question.id]);
        if (nextQuestion) {
          setSelectedQuestionId(nextQuestion.id);
        }
      }
      setActiveTab("interview");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Answer submission failed");
    } finally {
      setBusyLabel(null);
    }
  }

  async function generateFeedbackReport() {
    if (!sessionId) return;

    setError(null);
    setBusyLabel("Evaluating and generating report");

    try {
      await evaluateSession(sessionId);
      const nextReport = await generateReport(sessionId);
      setReport(nextReport);
      setActiveTab("report");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Report generation failed");
    } finally {
      setBusyLabel(null);
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark" aria-hidden="true">
            <Brain size={20} />
          </div>
          <div>
            <h1>AI Agent Interview Assistant</h1>
            <p>Resume-aware technical mock interview workspace</p>
          </div>
        </div>
        <div className="status-pill">
          {busyLabel ? (
            <Loader2 size={16} className="spin" />
          ) : backendOnline === false ? (
            <CircleAlert size={16} />
          ) : (
            <CheckCircle2 size={16} />
          )}
          {statusText}
        </div>
      </header>

      <div className="workspace">
        <aside className="panel setup-panel">
          <h2 className="panel-title">Interview Setup</h2>
          <div className="field">
            <label htmlFor="company">Company</label>
            <input
              id="company"
              value={companyName}
              onChange={(event) => setCompanyName(event.target.value)}
            />
          </div>
          <div className="field">
            <label htmlFor="role">Role</label>
            <input
              id="role"
              value={roleTitle}
              onChange={(event) => setRoleTitle(event.target.value)}
            />
          </div>
          <div className="field">
            <label htmlFor="jd">Job Description</label>
            <textarea
              id="jd"
              value={jobDescription}
              onChange={(event) => setJobDescription(event.target.value)}
            />
          </div>
          <div className="field">
            <label htmlFor="resume">Resume（必填）</label>
            <input
              id="resume"
              type="file"
              accept=".pdf,.txt,.md,.doc,.docx"
              onChange={(event) => {
                setResumeFile(event.target.files?.[0] ?? null);
              }}
            />
          </div>
          <div className="field">
            <label htmlFor="knowledgeFiles">Knowledge Files（可选，可多选）</label>
            <input
              id="knowledgeFiles"
              type="file"
              accept=".pdf,.txt,.md,.doc,.docx"
              multiple
              onChange={(event) => {
                const files = event.target.files;
                if (!files) {
                  setKnowledgeFiles([]);
                  return;
                }
                setKnowledgeFiles(Array.from(files));
              }}
            />
          </div>
          {error ? <div className="error">{error}</div> : null}
          <div className="button-row">
            <button className="btn btn-primary" onClick={runSetup} disabled={Boolean(busyLabel)}>
              <Play size={16} />
              Prepare
            </button>
          </div>
        </aside>

        <section className="panel main-panel">
          <nav className="tabs" aria-label="Workspace views">
            <button
              className={`tab ${activeTab === "plan" ? "tab-active" : ""}`}
              onClick={() => setActiveTab("plan")}
            >
              <FileText size={16} />
              Plan
            </button>
            <button
              className={`tab ${activeTab === "interview" ? "tab-active" : ""}`}
              onClick={() => setActiveTab("interview")}
            >
              <MessageSquareText size={16} />
              Interview
            </button>
            <button
              className={`tab ${activeTab === "report" ? "tab-active" : ""}`}
              onClick={() => setActiveTab("report")}
            >
              <CheckCircle2 size={16} />
              Report
            </button>
          </nav>

          <div className="content">
            {activeTab === "plan" ? (
              <PlanView
                plan={plan}
                selectedQuestionId={selectedQuestion?.id ?? null}
                onSelectQuestion={(questionId) => {
                  setSelectedQuestionId(questionId);
                  setActiveTab("interview");
                }}
              />
            ) : null}

            {activeTab === "interview" ? (
              <InterviewView
                questions={plan?.questions ?? []}
                selectedQuestion={selectedQuestion}
                selectedQuestionId={selectedQuestionId}
                answerDrafts={answerDrafts}
                submittedAnswers={submittedAnswers}
                followUp={followUp}
                onSelectQuestion={setSelectedQuestionId}
                onAnswerChange={(questionId, value) => {
                  setAnswerDrafts((current) => ({ ...current, [questionId]: value }));
                }}
                onSubmit={submitCurrentAnswer}
                onReport={generateFeedbackReport}
                busy={Boolean(busyLabel)}
              />
            ) : null}

            {activeTab === "report" ? <ReportView report={report} /> : null}
          </div>
        </section>
      </div>
    </main>
  );
}

function PlanView({
  plan,
  selectedQuestionId,
  onSelectQuestion,
}: {
  plan: InterviewPlanView | null;
  selectedQuestionId: string | null;
  onSelectQuestion: (questionId: string) => void;
}) {
  if (!plan) {
    return (
      <div className="notice">
        Prepare a session to generate a personalized interview plan.
      </div>
    );
  }

  return (
    <div className="grid-two">
      <div className="section">
        <h2>Question Plan</h2>
        <div className="question-list">
          {plan.questions.map((question, index) => (
            <button
              className={`question-item ${
                question.id === selectedQuestionId ? "question-item-active" : ""
              }`}
              key={question.id}
              onClick={() => onSelectQuestion(question.id)}
            >
              <div className="question-meta">
                <span className="chip">Q{index + 1}</span>
                <span className="chip">{question.topic}</span>
                <span className="chip">{question.difficulty}</span>
              </div>
              <div>{question.prompt}</div>
            </button>
          ))}
        </div>
      </div>
      <aside className="section">
        <h3>Candidate Storyline</h3>
        <p className="muted">{plan.candidate_storyline}</p>
        <h3>Deep Dives</h3>
        <div className="question-meta">
          {plan.planned_deep_dives.map((item) => (
            <span className="chip" key={item}>
              {item}
            </span>
          ))}
        </div>
      </aside>
    </div>
  );
}

function InterviewView({
  questions,
  selectedQuestion,
  selectedQuestionId,
  answerDrafts,
  submittedAnswers,
  followUp,
  onSelectQuestion,
  onAnswerChange,
  onSubmit,
  onReport,
  busy,
}: {
  questions: InterviewQuestionView[];
  selectedQuestion: InterviewQuestionView | null;
  selectedQuestionId: string | null;
  answerDrafts: Record<string, string>;
  submittedAnswers: Record<string, string>;
  followUp: InterviewQuestionView | null;
  onSelectQuestion: (questionId: string) => void;
  onAnswerChange: (questionId: string, value: string) => void;
  onSubmit: () => void;
  onReport: () => void;
  busy: boolean;
}) {
  const currentAnswer = selectedQuestion ? answerDrafts[selectedQuestion.id] ?? "" : "";
  const selectedQuestionIndex = selectedQuestion
    ? questions.findIndex((question) => question.id === selectedQuestion.id)
    : -1;

  return (
    <div className="chatbot-shell">
      <div className="chatbot-header">
        <div>
          <h2>Mock Interview</h2>
          <p>AI interviewer</p>
        </div>
        <div className="chatbot-status">
          <span className="online-dot" />
          {questions.length}/12 generated
        </div>
      </div>

      <div className="chatbot-thread">
        {questions.length === 0 ? (
          <div className="message-row assistant-row">
            <div className="message-avatar">AI</div>
            <div className="message-bubble assistant-message">
              Running the preparation graph. Questions will appear here one by one.
            </div>
          </div>
        ) : null}

        {questions.map((question, index) => {
          const submittedAnswer = submittedAnswers[question.id];
          const isSelected = question.id === selectedQuestionId;
          return (
            <div className="chat-turn" key={question.id}>
              <div className="message-row assistant-row">
                <div className="message-avatar">AI</div>
                <button
                  className={`message-bubble assistant-message ${
                    isSelected ? "message-active" : ""
                  }`}
                  onClick={() => onSelectQuestion(question.id)}
                >
                  <div className="question-meta">
                    <span className="chip">Q{index + 1}</span>
                    <span className="chip">{question.topic}</span>
                    <span className="chip">{question.difficulty}</span>
                  </div>
                  <p>{question.prompt}</p>
                </button>
              </div>

              {submittedAnswer ? (
                <div className="message-row candidate-row">
                  <div className="message-bubble candidate-message">
                    <p>{submittedAnswer}</p>
                  </div>
                  <div className="message-avatar candidate-avatar">You</div>
                </div>
              ) : null}
            </div>
          );
        })}

        {followUp ? (
          <div className="message-row assistant-row">
            <div className="message-avatar">AI</div>
            <div className="message-bubble assistant-message">
              <div className="question-meta">
                <span className="chip">Follow-up</span>
                <span className="chip">{followUp.topic}</span>
              </div>
              <p>{followUp.prompt}</p>
            </div>
          </div>
        ) : null}
      </div>

      <div className="chatbot-composer">
        <div className="composer-context">
          {selectedQuestion
            ? `Answering Q${selectedQuestionIndex + 1}`
            : "Waiting for a question"}
        </div>
        <textarea
          className="composer-input"
          value={currentAnswer}
          placeholder="Type your answer..."
          disabled={!selectedQuestion}
          onChange={(event) => {
            if (selectedQuestion) {
              onAnswerChange(selectedQuestion.id, event.target.value);
            }
          }}
        />
        <div className="composer-actions">
          <button
            className="btn btn-primary"
            onClick={onSubmit}
            disabled={busy || !selectedQuestion || !currentAnswer.trim()}
          >
            <Send size={16} />
            Send
          </button>
          <button className="btn btn-secondary" onClick={onReport} disabled={busy}>
            <CheckCircle2 size={16} />
            Report
          </button>
        </div>
      </div>
    </div>
  );
}

function ReportView({ report }: { report: string }) {
  if (!report) {
    return <div className="notice">Generate a report after submitting at least one answer.</div>;
  }

  return <div className="report-box">{report}</div>;
}
