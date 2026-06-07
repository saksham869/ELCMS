const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Employee {
  id: string;
  name: string;
  role: string;
  department: string;
  team_id: string;
  certification_target: string;
  current_practice_score: number;
  hours_studied: number;
  focus_hours_per_week: number;
  meeting_hours_per_week: number;
  weeks_until_exam: number;
  starting_score: number;
  preferred_study_time: string;
  manager_id: string;
}

export interface PipelineEvent {
  event: string;
  [key: string]: unknown;
}

export async function fetchHealth() {
  const res = await fetch(`${API_URL}/api/health`);
  return res.json();
}

export async function fetchEmployees(): Promise<{ employees: Employee[] }> {
  const res = await fetch(`${API_URL}/api/employees`);
  return res.json();
}

export async function fetchEmployee(employeeId: string): Promise<Employee> {
  const res = await fetch(`${API_URL}/api/employees/${employeeId}`);
  return res.json();
}

export async function fetchTeamDashboard(teamId: string) {
  const res = await fetch(`${API_URL}/api/team/${teamId}/dashboard`);
  return res.json();
}

export function streamPipeline(
  employeeId: string,
  onEvent: (event: PipelineEvent) => void,
  onDone?: () => void,
  onError?: (err: Error) => void
): () => void {
  const url = `${API_URL}/api/certify/${employeeId}/stream`;
  const eventSource = new EventSource(url);

  eventSource.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data) as PipelineEvent;
      onEvent(data);
      if (data.event === "pipeline_complete") {
        eventSource.close();
        onDone?.();
      }
    } catch {
      // ignore parse errors
    }
  };

  eventSource.onerror = (e) => {
    eventSource.close();
    onError?.(new Error("SSE connection error"));
    onDone?.();
  };

  return () => eventSource.close();
}

export function getVerdictColor(verdict: string): string {
  switch (verdict) {
    case "GO":
      return "text-green-400 bg-green-400/10 border-green-400/30";
    case "CONDITIONAL GO":
      return "text-amber-400 bg-amber-400/10 border-amber-400/30";
    case "APPROACHING":
      return "text-yellow-400 bg-yellow-400/10 border-yellow-400/30";
    case "NOT YET":
      return "text-red-400 bg-red-400/10 border-red-400/30";
    default:
      return "text-gray-400 bg-gray-400/10 border-gray-400/30";
  }
}

export function getScoreColor(score: number): string {
  if (score >= 75) return "#10b981";
  if (score >= 65) return "#f59e0b";
  if (score >= 55) return "#eab308";
  return "#ef4444";
}