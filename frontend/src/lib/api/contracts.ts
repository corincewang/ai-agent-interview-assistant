export type DocumentType =
  | "resume"
  | "knowledge_base"
  | "job_description"
  | "company_research"
  | "interview_intel";

export type InterviewMode = "frontend" | "backend" | "ai_agent" | "general_swe";

export interface CreateInterviewSessionRequest {
  company_name: string;
  role_title: string;
  job_description: string;
  mode: InterviewMode;
}

export interface CreateInterviewSessionResponse {
  session_id: string;
  company_name: string;
  role_title: string;
  mode: InterviewMode;
}

export interface UploadDocumentRequest {
  sessionId: string;
  documentType: DocumentType;
  file: File;
}

export interface CandidateProfileView {
  technicalSkills: string[];
  projectHighlights: string[];
  riskAreas: string[];
  followUpTargets: string[];
}

export interface InterviewQuestionView {
  id: string;
  prompt: string;
  topic: string;
  difficulty: "easy" | "medium" | "hard";
  expected_signals: string[];
  follow_up_strategy: string[];
}

export interface SubmitAnswerRequest {
  question_id: string;
  answer: string;
}

export interface SubmitAnswerResponse {
  session_id: string;
  follow_up_question: InterviewQuestionView | null;
}

export interface PrepareSessionResponse {
  session_id: string;
  interview_plan: InterviewPlanView;
}

export interface InterviewPlanView {
  session_id: string;
  mode: InterviewMode;
  questions: InterviewQuestionView[];
  rubric: Record<string, string>;
  candidate_storyline: string;
  planned_deep_dives: string[];
}

export interface InterviewReportView {
  sessionId: string;
  summary: string;
  scores: Record<string, number>;
  strengths: string[];
  weaknesses: string[];
  nextPracticeSteps: string[];
}
