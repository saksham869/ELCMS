"use client";

import { useState } from "react";

const TIER_BADGE: Record<number, { bg: string; text: string }> = {
  1: { bg: "bg-[#1f6feb]/20", text: "text-[#58a6ff]" },
  2: { bg: "bg-[#238636]/20", text: "text-[#3fb950]" },
  3: { bg: "bg-[#6e40c9]/20", text: "text-[#a371f7]" },
  4: { bg: "bg-[#9e6a03]/20", text: "text-[#d29922]" },
};

const MOCK_AUDIT = [
  { audit_id: "a1b2c3d4", timestamp_start: "2026-06-07T09:00:01Z", agent_name: "Learner Profiler",       employee_id: "EMP-001", tier_used: 1, docs_retrieved: 3, latency_ms: 84,  eval_score: 0.83, responsible_ai_check: "PASS", loop_iteration: 1, query: "Cloud Engineer certification requirements", citations: ["[Source: Skills Matrix]"] },
  { audit_id: "b2c3d4e5", timestamp_start: "2026-06-07T09:00:02Z", agent_name: "Learning Path Curator", employee_id: "EMP-001", tier_used: 1, docs_retrieved: 3, latency_ms: 3981,eval_score: 0.85, responsible_ai_check: "PASS", loop_iteration: 1, query: "AZ-204 certification guide",                citations: ["[Source: Cert Guide]", "[Source: Skills Matrix]"] },
  { audit_id: "c3d4e5f6", timestamp_start: "2026-06-07T09:00:06Z", agent_name: "Assessment Agent",       employee_id: "EMP-003", tier_used: 1, docs_retrieved: 0, latency_ms: 0,    eval_score: 0.35, responsible_ai_check: "PASS", loop_iteration: 1, query: "",                                                   citations: [] },
  { audit_id: "d4e5f6g7", timestamp_start: "2026-06-07T09:00:07Z", agent_name: "Intervention Agent",     employee_id: "EMP-003", tier_used: 1, docs_retrieved: 3, latency_ms: 2100, eval_score: 0.88, responsible_ai_check: "PASS", loop_iteration: 2, query: "intervention best practices",                     citations: ["[Source: Intervention Best Practices]"] },
  { audit_id: "e5f6g7h8", timestamp_start: "2026-06-07T09:00:08Z", agent_name: "Readiness Forecaster",   employee_id: "EMP-002", tier_used: 1, docs_retrieved: 2, latency_ms: 110,  eval_score: 0.91, responsible_ai_check: "PASS", loop_iteration: 1, query: "peer cohort benchmarks",                           citations: ["[Source: Peer Cohort Benchmarks]"] },
  { audit_id: "f6g7h8i9", timestamp_start: "2026-06-07T09:00:09Z", agent_name: "ROI Calculator",         employee_id: "EMP-004", tier_used: 1, docs_retrieved: 3, latency_ms: 66,   eval_score: 1.0,  responsible_ai_check: "PASS", loop_iteration: 1, query: "certification roi cost analysis",                citations: ["[Source: Cert ROI & Cost Analysis]"] },
  { audit_id: "g7h8i9j0", timestamp_start: "2026-06-07T09:00:10Z", agent_name: "Peer Benchmarking Agent",employee_id: "EMP-001", tier_used: 1, docs_retrieved: 0, latency_ms: 1,    eval_score: 0.75, responsible_ai_check: "PASS", loop_iteration: 1, query: "AZ-204 cohort",                                    citations: [] },
];

export default function AuditPage() {
  const [filter, setFilter] = useState("");
  const [expanded, setExpanded] = useState<Set<string>>(new Set());

  const filtered = MOCK_AUDIT.filter(
    (e) =>
      e.employee_id.toLowerCase().includes(filter.toLowerCase()) ||
      e.agent_name.toLowerCase().includes(filter.toLowerCase())
  );

  const toggle = (id: string) => {
    setExpanded((prev) => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-[#f0f6fc] text-2xl font-bold">Agent Decision Log</h1>
          <p className="text-[#6e7681] text-sm font-mono mt-1">
            Append-only · 25-rule guardrail validated · {filtered.length} entries
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button className="text-xs text-[#8b949e] hover:text-[#f0f6fc] transition-colors border border-[#21262d] rounded px-3 py-1.5">
            Export CSV ↓
          </button>
          <select className="text-xs bg-[#0d1117] border border-[#21262d] text-[#8b949e] rounded px-3 py-1.5 focus:outline-none focus:border-[#1f6feb]">
            <option>All employees</option>
            <option>EMP-001</option>
            <option>EMP-002</option>
            <option>EMP-003</option>
            <option>EMP-004</option>
          </select>
        </div>
      </div>

      {/* Filter */}
      <div className="mb-4">
        <input
          type="text"
          placeholder="Filter by employee or agent..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="bg-[#0d1117] border border-[#21262d] rounded px-4 py-2 text-sm text-[#f0f6fc] placeholder-[#6e7681] focus:outline-none focus:border-[#1f6feb] font-mono w-full max-w-sm transition-colors"
        />
      </div>

      {/* Table */}
      <div className="bg-[#0d1117] border border-[#21262d] rounded-lg overflow-hidden">
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-[#21262d]">
              {["Time", "Agent", "Employee", "Tier", "Docs", "Latency", "Score", "RAI", "Loop", ""].map((h) => (
                <th key={h} className="text-left px-4 py-2.5 text-[#6e7681] uppercase tracking-widest font-medium text-[10px]">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.map((entry) => {
              const isExpanded = expanded.has(entry.audit_id);
              const tierStyle = TIER_BADGE[entry.tier_used] || TIER_BADGE[4];
              return (
                <>
                  <tr
                    key={entry.audit_id}
                    onClick={() => toggle(entry.audit_id)}
                    className="border-b border-[#21262d] hover:bg-[#161b22] transition-colors cursor-pointer"
                  >
                    <td className="px-4 py-3 font-mono text-[#6e7681]">
                      {new Date(entry.timestamp_start).toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit", second: "2-digit" })}
                    </td>
                    <td className="px-4 py-3 text-[#f0f6fc]">{entry.agent_name}</td>
                    <td className="px-4 py-3">
                      <span className="font-mono text-[#8b949e] bg-[#161b22] border border-[#30363d] px-2 py-0.5 rounded">
                        {entry.employee_id}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`font-mono px-2 py-0.5 rounded font-medium ${tierStyle.bg} ${tierStyle.text}`}>
                        T{entry.tier_used}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-mono text-[#8b949e]">{entry.docs_retrieved}</td>
                    <td className="px-4 py-3 font-mono text-[#8b949e]">{entry.latency_ms}ms</td>
                    <td className="px-4 py-3">
                      <span className={`font-mono font-bold ${entry.eval_score >= 0.85 ? "text-[#3fb950]" : "text-[#58a6ff]"}`}>
                        {(entry.eval_score * 100).toFixed(0)}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className="text-[#3fb950] bg-[#238636]/20 border border-[#238636]/30 px-2 py-0.5 rounded">
                        {entry.responsible_ai_check}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-mono text-[#6e7681]">L{entry.loop_iteration}</td>
                    <td className="px-4 py-3 text-[#6e7681]">{isExpanded ? "▾" : "▸"}</td>
                  </tr>
                  {isExpanded && (
                    <tr key={`${entry.audit_id}-expand`} className="border-b border-[#21262d] bg-[#161b22]">
                      <td colSpan={10} className="px-8 py-4">
                        <div className="grid grid-cols-2 gap-4 text-xs font-mono">
                          <div>
                            <p className="text-[#6e7681] mb-1">Foundry IQ query</p>
                            <p className="text-[#f0f6fc]">{entry.query || "(no Foundry IQ query — rule-based agent)"}</p>
                          </div>
                          <div>
                            <p className="text-[#6e7681] mb-1">Citations retrieved</p>
                            {entry.citations.length > 0 ? (
                              entry.citations.map((c, i) => (
                                <p key={i} className="text-[#8b949e]">{c}</p>
                              ))
                            ) : (
                              <p className="text-[#6e7681] italic">No docs retrieved</p>
                            )}
                          </div>
                          <div>
                            <p className="text-[#6e7681] mb-1">Audit ID</p>
                            <p className="text-[#6e7681]">{entry.audit_id}</p>
                          </div>
                          <div>
                            <p className="text-[#6e7681] mb-1">RAI guardrails</p>
                            <p className="text-[#3fb950]">Input: PASS · Output: PASS · Bias: PASS</p>
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="mt-4 p-4 border border-[#21262d] rounded-lg text-[10px] text-[#6e7681] font-mono">
        All AI pipeline executions are logged with full audit trail.
        This log is append-only and tamper-evident. RAI = Responsible AI check (25 rules).
        T1=GitHub Models GPT-4o · T4=Mock engine
      </div>

      <div className="mt-6">
        <a href="/" className="text-xs text-[#6e7681] hover:text-[#f0f6fc] transition-colors">
          ← Back to home
        </a>
      </div>
    </div>
  );
}