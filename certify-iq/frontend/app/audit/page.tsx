"use client";

import { useState } from "react";

const MOCK_AUDIT = [
  {
    audit_id: "a1b2c3d4",
    timestamp_start: "2026-06-07T09:00:01Z",
    agent_name: "Learner Profiler",
    employee_id: "EMP-001",
    docs_retrieved: 3,
    latency_ms: 84,
    eval_score: 0.83,
    responsible_ai_check: "PASS",
    loop_iteration: 1,
  },
  {
    audit_id: "b2c3d4e5",
    timestamp_start: "2026-06-07T09:00:02Z",
    agent_name: "Learning Path Curator",
    employee_id: "EMP-001",
    docs_retrieved: 3,
    latency_ms: 108,
    eval_score: 0.85,
    responsible_ai_check: "PASS",
    loop_iteration: 1,
  },
  {
    audit_id: "c3d4e5f6",
    timestamp_start: "2026-06-07T09:00:03Z",
    agent_name: "Assessment Agent",
    employee_id: "EMP-003",
    docs_retrieved: 2,
    latency_ms: 96,
    eval_score: 0.87,
    responsible_ai_check: "PASS",
    loop_iteration: 2,
  },
  {
    audit_id: "d4e5f6g7",
    timestamp_start: "2026-06-07T09:00:04Z",
    agent_name: "Intervention Agent",
    employee_id: "EMP-003",
    docs_retrieved: 2,
    latency_ms: 150,
    eval_score: 0.88,
    responsible_ai_check: "PASS",
    loop_iteration: 2,
  },
  {
    audit_id: "e5f6g7h8",
    timestamp_start: "2026-06-07T09:00:05Z",
    agent_name: "Readiness Forecaster",
    employee_id: "EMP-002",
    docs_retrieved: 2,
    latency_ms: 110,
    eval_score: 0.91,
    responsible_ai_check: "PASS",
    loop_iteration: 1,
  },
];

export default function AuditPage() {
  const [filter, setFilter] = useState("");

  const filtered = MOCK_AUDIT.filter(
    (entry) =>
      entry.employee_id.toLowerCase().includes(filter.toLowerCase()) ||
      entry.agent_name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Audit Trail</h1>
          <p className="text-gray-400 mt-1">Append-only agent execution log — CertifyIQ Responsible AI</p>
        </div>
        <div className="text-sm text-gray-500">
          {filtered.length} entries
        </div>
      </div>

      <div className="mb-4">
        <input
          type="text"
          placeholder="Filter by employee ID or agent name..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="bg-[#0d1429] border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white placeholder-gray-600 w-full max-w-md focus:outline-none focus:border-blue-500/50"
        />
      </div>

      <div className="bg-[#0d1429] border border-white/10 rounded-2xl overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-gray-500 border-b border-white/10 bg-white/5">
              <th className="text-left px-4 py-3">Audit ID</th>
              <th className="text-left px-4 py-3">Timestamp</th>
              <th className="text-left px-4 py-3">Agent</th>
              <th className="text-left px-4 py-3">Employee</th>
              <th className="text-left px-4 py-3">Docs</th>
              <th className="text-left px-4 py-3">Latency</th>
              <th className="text-left px-4 py-3">Eval</th>
              <th className="text-left px-4 py-3">RAI</th>
              <th className="text-left px-4 py-3">Loop</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((entry) => (
              <tr key={entry.audit_id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td className="px-4 py-3 font-mono text-xs text-gray-500">{entry.audit_id}</td>
                <td className="px-4 py-3 text-gray-400 text-xs">
                  {new Date(entry.timestamp_start).toLocaleTimeString()}
                </td>
                <td className="px-4 py-3 text-white">{entry.agent_name}</td>
                <td className="px-4 py-3">
                  <span className="text-xs font-mono bg-white/5 border border-white/10 px-2 py-0.5 rounded text-gray-300">
                    {entry.employee_id}
                  </span>
                </td>
                <td className="px-4 py-3 text-gray-400">{entry.docs_retrieved}</td>
                <td className="px-4 py-3 text-gray-400">{entry.latency_ms}ms</td>
                <td className="px-4 py-3">
                  <span
                    className={`text-xs font-bold ${
                      entry.eval_score >= 0.85 ? "text-green-400" : "text-blue-400"
                    }`}
                  >
                    {(entry.eval_score * 100).toFixed(0)}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <span className="text-xs text-green-400 bg-green-500/10 border border-green-500/20 px-2 py-0.5 rounded">
                    {entry.responsible_ai_check}
                  </span>
                </td>
                <td className="px-4 py-3 text-gray-500">{entry.loop_iteration}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-4 p-4 bg-white/5 rounded-xl text-xs text-gray-500">
        All AI pipeline executions are logged with full audit trail including agent name, employee ID,
        docs retrieved, latency, evaluation score, and responsible AI check results.
        This log is append-only and cannot be modified.
      </div>

      <div className="mt-6">
        <a href="/" className="text-sm text-gray-500 hover:text-white transition-colors">
          ← Back to home
        </a>
      </div>
    </div>
  );
}