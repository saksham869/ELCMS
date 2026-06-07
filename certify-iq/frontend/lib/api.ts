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

export interface QueryResult {
  question: string;
  answer: string;
  relevant_employees: string[];
  action: string;
  citations: string[];
  confidence: number;
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

export async function queryNaturalLanguage(question: string): Promise<QueryResult> {
  const res = await fetch(`${API_URL}/api/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
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

  eventSource.onerror = () => {
    eventSource.close();
    onError?.(new Error("SSE connection error"));
    onDone?.();
  };

  return () => eventSource.close();
}

export function getVerdictStyle(verdict: string): { text: string; bg: string; border: string } {
  switch (verdict) {
    case "GO":
      return { text: "text-[#3fb950]", bg: "bg-[#238636]/20", border: "border-[#238636]/50" };
    case "CONDITIONAL GO":
      return { text: "text-[#d29922]", bg: "bg-[#9e6a03]/20", border: "border-[#9e6a03]/50" };
    case "APPROACHING":
      return { text: "text-[#d29922]", bg: "bg-[#9e6a03]/10", border: "border-[#9e6a03]/30" };
    case "NOT YET":
      return { text: "text-[#f85149]", bg: "bg-[#da3633]/20", border: "border-[#da3633]/50" };
    default:
      return { text: "text-[#8b949e]", bg: "bg-[#30363d]/20", border: "border-[#30363d]/50" };
  }
}

export function getVerdictColor(verdict: string): string {
  const s = getVerdictStyle(verdict);
  return `${s.text} ${s.bg} ${s.border}`;
}

export function getAvatarColor(verdict: string): string {
  switch (verdict) {
    case "GO": return "bg-[#238636]";
    case "CONDITIONAL GO": return "bg-[#9e6a03]";
    case "APPROACHING": return "bg-[#9e6a03]";
    case "NOT YET": return "bg-[#da3633]";
    default: return "bg-[#30363d]";
  }
}

export function getScoreColor(score: number): string {
  if (score >= 75) return "#3fb950";
  if (score >= 65) return "#d29922";
  if (score >= 55) return "#d29922";
  return "#f85149";
}

export function getInitials(name: string): string {
  return name.split(" ").map(n => n[0]).join("").toUpperCase().slice(0, 2);
}

export const ROI_PER_EMP: Record<string, number> = {
  "EMP-001": 170,
  "EMP-002": 146,
  "EMP-003": 188,
  "EMP-004": 158,
};

export const VERDICTS: Record<string, string> = {
  "EMP-001": "APPROACHING",
  "EMP-002": "GO",
  "EMP-003": "NOT YET",
  "EMP-004": "APPROACHING",
};

export const PERCENTILES: Record<string, number> = {
  "EMP-001": 46,
  "EMP-002": 72,
  "EMP-003": 22,
  "EMP-004": 58,
};

export const STATIC_EMPLOYEES: Employee[] = [
  { id: "EMP-001", name: "Alex Chen", role: "Cloud Engineer", department: "Cloud Platform", team_id: "TEAM-A", certification_target: "AZ-204", current_practice_score: 62, hours_studied: 8, focus_hours_per_week: 14, meeting_hours_per_week: 18, weeks_until_exam: 4, starting_score: 48, preferred_study_time: "Morning", manager_id: "MGR-001" },
  { id: "EMP-002", name: "Jordan Smith", role: "DevOps Engineer", department: "Infrastructure", team_id: "TEAM-A", certification_target: "AZ-400", current_practice_score: 78, hours_studied: 18, focus_hours_per_week: 20, meeting_hours_per_week: 12, weeks_until_exam: 3, starting_score: 55, preferred_study_time: "Evening", manager_id: "MGR-001" },
  { id: "EMP-003", name: "Morgan Lee", role: "Data Engineer", department: "Analytics", team_id: "TEAM-B", certification_target: "DP-203", current_practice_score: 45, hours_studied: 5, focus_hours_per_week: 8, meeting_hours_per_week: 24, weeks_until_exam: 5, starting_score: 38, preferred_study_time: "Morning", manager_id: "MGR-002" },
  { id: "EMP-004", name: "Riley Park", role: "AI Engineer", department: "AI & Cognitive", team_id: "TEAM-B", certification_target: "AI-102", current_practice_score: 71, hours_studied: 14, focus_hours_per_week: 18, meeting_hours_per_week: 15, weeks_until_exam: 3, starting_score: 58, preferred_study_time: "Afternoon", manager_id: "MGR-002" },
];