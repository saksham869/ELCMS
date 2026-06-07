"use client";

import { useEffect, useState } from "react";
import { fetchEmployees, getVerdictColor, getScoreColor, type Employee } from "@/lib/api";

const VERDICTS: Record<string, string> = {
  "EMP-001": "APPROACHING",
  "EMP-002": "GO",
  "EMP-003": "NOT YET",
  "EMP-004": "APPROACHING",
};

const PERCENTILES: Record<string, number> = {
  "EMP-001": 46,
  "EMP-002": 72,
  "EMP-003": 22,
  "EMP-004": 58,
};

export default function Home() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEmployees()
      .then((data) => setEmployees(data.employees))
      .catch(() => {
        // Fallback to static data if backend not running
        setEmployees([
          { id: "EMP-001", name: "Alex Chen", role: "Cloud Engineer", department: "Cloud Platform", team_id: "TEAM-A", certification_target: "AZ-204", current_practice_score: 62, hours_studied: 8, focus_hours_per_week: 14, meeting_hours_per_week: 18, weeks_until_exam: 4, starting_score: 48, preferred_study_time: "Morning", manager_id: "MGR-001" },
          { id: "EMP-002", name: "Jordan Smith", role: "DevOps Engineer", department: "Infrastructure", team_id: "TEAM-A", certification_target: "AZ-400", current_practice_score: 78, hours_studied: 18, focus_hours_per_week: 20, meeting_hours_per_week: 12, weeks_until_exam: 3, starting_score: 55, preferred_study_time: "Evening", manager_id: "MGR-001" },
          { id: "EMP-003", name: "Morgan Lee", role: "Data Engineer", department: "Analytics", team_id: "TEAM-B", certification_target: "DP-203", current_practice_score: 45, hours_studied: 5, focus_hours_per_week: 8, meeting_hours_per_week: 24, weeks_until_exam: 5, starting_score: 38, preferred_study_time: "Morning", manager_id: "MGR-002" },
          { id: "EMP-004", name: "Riley Park", role: "AI Engineer", department: "AI & Cognitive", team_id: "TEAM-B", certification_target: "AI-102", current_practice_score: 71, hours_studied: 14, focus_hours_per_week: 18, meeting_hours_per_week: 15, weeks_until_exam: 3, starting_score: 58, preferred_study_time: "Afternoon", manager_id: "MGR-002" },
        ]);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-6 py-12">
      {/* Header */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/30 rounded-full px-4 py-1.5 text-sm text-blue-300 mb-6">
          <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
          Hackathon Build — Mock Mode Active
        </div>
        <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 via-purple-400 to-teal-400 bg-clip-text text-transparent">
          CertifyIQ
        </h1>
        <p className="text-xl text-gray-400 max-w-2xl mx-auto">
          Enterprise Workforce Intelligence — 10 AI Reasoning Agents powered by Azure AI Foundry IQ
        </p>
      </div>

      {/* Badge Row */}
      <div className="flex flex-wrap justify-center gap-3 mb-8">
        {[
          { label: "10 Reasoning Agents", color: "blue" },
          { label: "Azure Foundry IQ", color: "purple" },
          { label: "25 Guardrails", color: "green" },
          { label: "4-Tier LLM Fallback", color: "orange" },
          { label: "Peer Benchmarking", color: "teal" },
        ].map((badge) => (
          <span
            key={badge.label}
            className={`px-3 py-1 rounded-full text-sm font-medium border
              ${badge.color === "blue" ? "bg-blue-500/10 text-blue-300 border-blue-500/30" : ""}
              ${badge.color === "purple" ? "bg-purple-500/10 text-purple-300 border-purple-500/30" : ""}
              ${badge.color === "green" ? "bg-green-500/10 text-green-300 border-green-500/30" : ""}
              ${badge.color === "orange" ? "bg-orange-500/10 text-orange-300 border-orange-500/30" : ""}
              ${badge.color === "teal" ? "bg-teal-500/10 text-teal-300 border-teal-500/30" : ""}
            `}
          >
            {badge.label}
          </span>
        ))}
      </div>

      {/* Stats Bar */}
      <div className="flex flex-wrap justify-center gap-6 mb-12 text-sm text-gray-500">
        <span>15 Certifications</span>
        <span className="text-gray-700">·</span>
        <span>50-member Cohort</span>
        <span className="text-gray-700">·</span>
        <span>12 Knowledge Docs</span>
        <span className="text-gray-700">·</span>
        <span>Sub-500ms Mock Mode</span>
      </div>

      {/* Employee Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-[#0d1429] border border-white/10 rounded-2xl p-6 animate-pulse h-64" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {employees.map((emp) => {
            const verdict = VERDICTS[emp.id] || "APPROACHING";
            const percentile = PERCENTILES[emp.id] || 50;
            const scoreColor = getScoreColor(emp.current_practice_score);
            const verdictStyles = getVerdictColor(verdict);

            return (
              <div
                key={emp.id}
                className="bg-[#0d1429] border border-white/10 rounded-2xl p-6 hover:border-white/20 transition-all hover:shadow-lg hover:shadow-blue-500/5"
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-white">{emp.name}</h3>
                    <p className="text-sm text-gray-400">{emp.role}</p>
                    <p className="text-xs text-gray-600 mt-1">{emp.department}</p>
                  </div>
                  <div className="text-right">
                    <div
                      className="w-14 h-14 rounded-full border-4 flex items-center justify-center text-lg font-bold"
                      style={{ borderColor: scoreColor, color: scoreColor }}
                    >
                      {emp.current_practice_score}
                    </div>
                    <p className="text-xs text-gray-500 mt-1">score</p>
                  </div>
                </div>

                <div className="flex items-center gap-2 mb-4">
                  <span className="text-xs font-mono bg-white/5 border border-white/10 px-2 py-1 rounded text-gray-300">
                    {emp.certification_target}
                  </span>
                  <span className={`text-xs px-2 py-1 rounded border font-medium ${verdictStyles}`}>
                    {verdict}
                  </span>
                  <span className="text-xs bg-teal-500/10 text-teal-300 border border-teal-500/30 px-2 py-1 rounded">
                    P{percentile}
                  </span>
                </div>

                <div className="grid grid-cols-3 gap-3 mb-4 text-center">
                  <div>
                    <p className="text-sm font-semibold text-white">{emp.hours_studied}h</p>
                    <p className="text-xs text-gray-500">studied</p>
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-white">{emp.weeks_until_exam}w</p>
                    <p className="text-xs text-gray-500">to exam</p>
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-white">{emp.meeting_hours_per_week}h</p>
                    <p className="text-xs text-gray-500">meetings</p>
                  </div>
                </div>

                <a
                  href={`/certify/${emp.id}`}
                  className="block w-full text-center bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium py-2.5 rounded-xl transition-colors"
                >
                  Run CertifyIQ Analysis
                </a>
              </div>
            );
          })}
        </div>
      )}

      {/* Bottom nav */}
      <div className="mt-12 flex flex-wrap justify-center gap-4">
        <a
          href="/dashboard"
          className="px-6 py-3 bg-purple-600/20 border border-purple-500/30 text-purple-300 rounded-xl hover:bg-purple-600/30 transition-colors text-sm font-medium"
        >
          Manager Dashboard
        </a>
        <a
          href="/roi"
          className="px-6 py-3 bg-green-600/20 border border-green-500/30 text-green-300 rounded-xl hover:bg-green-600/30 transition-colors text-sm font-medium"
        >
          ROI Calculator
        </a>
        <a
          href="/audit"
          className="px-6 py-3 bg-gray-600/20 border border-gray-500/30 text-gray-300 rounded-xl hover:bg-gray-600/30 transition-colors text-sm font-medium"
        >
          Audit Trail
        </a>
      </div>
    </div>
  );
}