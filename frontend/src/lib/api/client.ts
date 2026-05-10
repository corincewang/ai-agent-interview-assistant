import {
  CreateInterviewSessionRequest,
  CreateInterviewSessionResponse,
  DocumentType,
  PrepareSessionResponse,
  SubmitAnswerRequest,
  SubmitAnswerResponse,
} from "./contracts";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE}/health`);
    return response.ok;
  } catch {
    return false;
  }
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function createInterviewSession(
  payload: CreateInterviewSessionRequest,
): Promise<CreateInterviewSessionResponse> {
  return requestJson<CreateInterviewSessionResponse>("/interview-sessions", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function uploadDocument(
  sessionId: string,
  documentType: DocumentType,
  file: File,
): Promise<void> {
  const form = new FormData();
  form.append("file", file);

  const response = await fetch(
    `${API_BASE}/interview-sessions/${sessionId}/documents?document_type=${documentType}`,
    {
      method: "POST",
      body: form,
    },
  );

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Upload failed: ${response.status}`);
  }
}

export async function prepareInterviewSession(
  sessionId: string,
): Promise<PrepareSessionResponse> {
  return requestJson<PrepareSessionResponse>(
    `/interview-sessions/${sessionId}/prepare`,
    { method: "POST" },
  );
}

export async function submitAnswer(
  sessionId: string,
  payload: SubmitAnswerRequest,
): Promise<SubmitAnswerResponse> {
  return requestJson<SubmitAnswerResponse>(
    `/interview-sessions/${sessionId}/turns`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );
}

export async function evaluateSession(sessionId: string): Promise<void> {
  await requestJson(`/interview-sessions/${sessionId}/evaluate`, {
    method: "POST",
  });
}

export async function generateReport(sessionId: string): Promise<string> {
  const response = await requestJson<{ report: string }>(
    `/interview-sessions/${sessionId}/report`,
    { method: "POST" },
  );
  return response.report;
}
