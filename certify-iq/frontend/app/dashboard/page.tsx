"use client";

import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { fetchEmployees, getVerdictColor, getScoreColor, type Employee } from "@/lib/api";

const VERDICTS: Record<string, string> = {
  "EMP-001": "APPROACHING",
  "EMP-002": "GO",
  "EMP-003": "NOT YET",
  "EMP-004": "APPROACHING",
};

const ROI_PER_EMP: Record<string, number> = {
  "EMP-001": 170,
  "EMP-002": 146,
  "EMP-003": 188,
  "EMP-004": 158,
};

export default function DashboardPage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEmployees()
      .then((d) => setEmployees(d.employees))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const verdictCounts = employees.reduce(
    (acc, emp) => {
      const v = VERDICTS[emp.id] || "APPROACHING";
      acc[v] = (acc[v] || 0) + 1;
      return acc;
    },
    {} as Record<string, number>
  );

  const teamReadiness =
    employees.length > 0
      ? Math.round((employees.filter((e) => VERDICTS[e.id] === "GO").length / employees.length) * 100)
      : 0;

  const totalROI = employees.reduce((sum, emp) => sum + (ROI_PER_EMP[emp.id] || 0), 0);

  const chartData = employees.map((emp) => ({
    name: emp.name.split(" ")[0],
    score: emp.current_practice_score,
    threshold: 75,
  }));

  const atRisk = employees.filter(
    (e) => VERDICTS[e.id] === "NOT YET" || e.meeting_hours_per_week > 22
  );

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Manager Dashboard</h1>
        <p className="text-gray-400 mt-1">Team certification readiness overview — CertifyIQ v3.0</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        {[
          { label: "Total", value: employees.length, color: "blue" },
          { label: "GO", value: verdictCounts["GO"] || 0, color: "green" },
          { label: "CONDITIONAL", value: (verdictCounts["CONDITIONAL GO"] || 0), color: "amber" },
          { label: "NOT YET", value: verdictCounts["NOT YET"] || 0, color: "red" },
          { label: "Team Readiness", value: `${teamReadiness}%`, color: "teal" },
          { label: "Total ROI", value: `$${totalROI}`, color: "purple" },
        ].map((stat) => (
          <div
            key={stat.label}
            className={`bg-[#0d1429] border rounded-xl p-4 text-center
              ${stat.color === "green" ? "border-green-500/20" : ""}
              ${stat.color === "red" ? "border-red-500/20" : ""}
              ${stat.color === "amber" ? "border-amber-500/20" : ""}
              ${stat.color === "blue" ? "border-blue-500/20" : ""}
              ${stat.color === "teal" ? "border-teal-500/20" : ""}
              ${stat.color === "purple" ? "border-purple-500/20" : ""}
            `}
          >
            <p
              className={`text-2xl font-bold
                ${stat.color === "green" ? "text-green-400" : ""}
                ${stat.color === "red" ? "text-red-400" : ""}
                ${stat.color === "amber" ? "text-amber-400" : ""}
                ${stat.color === "blue" ? "text-blue-400" : ""}
                ${stat.color === "teal" ? "text-teal-400" : ""}
                ${stat.color === "purple" ? "text-purple-400" : ""}
              `}
            >
              {stat.value}
            </p>
            <p className="text-xs text-gray-500 mt-1">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Chart */}
      <div className="bg-[#0d1429] border border-white/10 rounded-2xl p-6 mb-6">
        <h2 className="font-semibold text-white mb-4">Team Readiness Chart</h2>
        {!loading && (
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
              <XAxis dataKey="name" tick={{ fill: "#9ca3af", fontSize: 12 }} />
              <YAxis tick={{ fill: "#9ca3af", fontSize: 12 }} domain={[0, 100]} />
              <Tooltip
                contentStyle={{ background: "#0d1429", border: "1px solid #ffffff20", borderRadius: "8px" }}
                labelStyle={{ color: "#fff" }}
              />
              <Bar dataKey="score" name="Practice Score" radius={[4, 4, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell
                    key={index}
                    fill={getScoreColor(entry.score)}
                  />
                ))}
              </Bar>
              <Bar dataKey="threshold" name="Pass Threshold" fill="#ffffff20" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* ROI Summary */}
      <div className="bg-[#0d1429] border border-green-500/20 rounded-2xl p-6 mb-6">
        <h2 className="font-semibold text-white mb-2">ROI Summary</h2>
        <p className="text-green-300 text-sm">
          CertifyIQ saves ${totalROI} across {employees.length} employees vs unguided exam prep.
          Guided pass rate: 89% vs unguided: 58%. Includes reduced retake costs + productivity recovery.
        </p>
      </div>

      {/* At-Risk Table */}
      {atRisk.length > 0 && (
        <div className="bg-[#0d1429] border border-red-500/20 rounded-2xl p-6 mb-6">
          <h2 className="font-semibold text-white mb-4">Intervention Required</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-gray-500 border-b border-white/5">
                  <th className="text-left pb-2">Name</th>
                  <th className="text-left pb-2">Cert</th>
                  <th className="text-left pb-2">Score</th>
                  <th className="text-left pb-2">Meetings/wk</th>
                  <th className="text-left pb-2">Verdict</th>
                  <th className="text-left pb-2">Action</th>
                </tr>
              </thead>
              <tbody>
                {atRisk.map((emp) => (
                  <tr key={emp.id} className="border-b border-white/5">
                    <td className="py-2 text-white">{emp.name}</td>
                    <td className="py-2 text-gray-400">{emp.certification_target}</td>
                    <td className="py-2" style={{ color: getScoreColor(emp.current_practice_score) }}>
                      {emp.current_practice_score}%
                    </td>
                    <td className={`py-2 ${emp.meeting_hours_per_week > 22 ? "text-orange-400" : "text-gray-400"}`}>
                      {emp.meeting_hours_per_week}h
                    </td>
                    <td className="py-2">
                      <span className={`px-2 py-0.5 rounded border text-xs ${getVerdictColor(VERDICTS[emp.id] || "")}`}>
                        {VERDICTS[emp.id]}
                      </span>
                    </td>
                    <td className="py-2">
                      <a
                        href={`/certify/${emp.id}`}
                        className="text-blue-400 hover:text-blue-300 text-xs"
                      >
                        Run Analysis →
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <a href="/" className="text-sm text-gray-500 hover:text-white transition-colors">
        ← Back to home
      </a>
    </div>
  );
}