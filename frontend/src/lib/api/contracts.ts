export type DocumentType =
  | "resume"
  | "knowledge_base"
  | "job_description"
  | "company_research"
  | "interview_intel";

export type InterviewMode = "frontend" | "backend" | "ai_agent" | "general_swe";

export interface CreateInterviewSessionRequest {
  companyName: string;
  roleTitle: string;
  jobDescription: string;
  mode: InterviewMode;
}

export interface CreateInterviewSessionResponse {
  sessionId: string;
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
  expectedSignals: string[];
}

export interface SubmitAnswerRequest {
  sessionId: string;
  questionId: string;
  answer: string;
}

export interface SubmitAnswerResponse {
  nextQuestion: InterviewQuestionView | null;
  followUpQuestion: InterviewQuestionView | null;
}

export interface InterviewReportView {
  sessionId: string;
  summary: string;
  scores: Record<string, number>;
  strengths: string[];
  weaknesses: string[];
  nextPracticeSteps: string[];
}

