"use client";

import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell, ReferenceLine,
} from "recharts";
import { fetchEmployees, getVerdictStyle, getScoreColor, VERDICTS, ROI_PER_EMP, PERCENTILES, type Employee } from "@/lib/api";

export default function DashboardPage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEmployees()
      .then((d) => setEmployees(d.employees))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const verdictCounts = employees.reduce((acc, emp) => {
    const v = VERDICTS[emp.id] || "APPROACHING";
    acc[v] = (acc[v] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const goCount = verdictCounts["GO"] || 0;
  const conditionalCount = verdictCounts["CONDITIONAL GO"] || 0;
  const approachingCount = verdictCounts["APPROACHING"] || 0;
  const notYetCount = verdictCounts["NOT YET"] || 0;
  const teamReadiness = employees.length > 0
    ? Math.round((goCount / employees.length) * 100)
    : 0;
  const totalROI = employees.reduce((sum, emp) => sum + (ROI_PER_EMP[emp.id] || 0), 0);

  const chartData = employees.map((emp) => ({
    name: emp.name.split(" ")[0],
    score: emp.current_practice_score,
    threshold: 75,
  }));

  const atRisk = employees.filter((e) => VERDICTS[e.id] === "NOT YET" || e.meeting_hours_per_week > 22);

  const STATS = [
    { label: "Readiness", value: `${teamReadiness}%`, color: teamReadiness >= 50 ? "#3fb950" : "#f85149" },
    { label: "ROI Saved", value: `$${totalROI}`, color: "#3fb950" },
    { label: "At Risk", value: `${notYetCount + (atRisk.length - notYetCount)} emp`, color: notYetCount > 0 ? "#f85149" : "#3fb950" },
    { label: "Total Reviewed", value: `${employees.length}`, color: "#f0f6fc" },
    { label: "GO Count", value: `${goCount}`, color: "#3fb950" },
    { label: "Conditional", value: `${conditionalCount + approachingCount}`, color: "#d29922" },
  ];

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-[#f0f6fc] text-2xl font-bold">Team Certification Intelligence</h1>
        <p className="text-[#6e7681] text-sm font-mono mt-1">
          Last analyzed · {new Date().toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })} · {employees.length} employees
        </p>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-6 gap-3 mb-8">
        {STATS.map((stat) => (
          <div key={stat.label} className="bg-[#0d1117] border border-[#21262d] rounded-lg p-4">
            <p className="text-2xl font-mono font-bold" style={{ color: stat.color }}>
              {stat.value}
            </p>
            <p className="text-[#6e7681] text-xs uppercase tracking-widest mt-1">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Chart */}
      <div className="bg-[#0d1117] border border-[#21262d] rounded-lg p-6 mb-6">
        <p className="text-[#f0f6fc] text-sm font-semibold mb-4">Score vs 75% pass threshold</p>
        {!loading && chartData.length > 0 && (
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={chartData} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#21262d" vertical={false} />
              <XAxis
                dataKey="name"
                tick={{ fill: "#6e7681", fontSize: 11 }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                tick={{ fill: "#6e7681", fontSize: 11 }}
                domain={[0, 100]}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                contentStyle={{
                  background: "#0d1117",
                  border: "1px solid #21262d",
                  borderRadius: "6px",
                  fontSize: "12px",
                }}
                labelStyle={{ color: "#f0f6fc" }}
                itemStyle={{ color: "#8b949e" }}
              />
              <ReferenceLine y={75} stroke="#da3633" strokeDasharray="4 4" label={{ value: "75% pass", fill: "#da3633", fontSize: 10 }} />
              <Bar dataKey="score" name="Practice Score" radius={[3, 3, 0, 0]} maxBarSize={40}>
                {chartData.map((entry, i) => (
                  <Cell key={i} fill={getScoreColor(entry.score)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* ROI summary */}
      <div className="bg-[#0d1117] border border-[#21262d] rounded-lg p-4 mb-6">
        <p className="text-[#3fb950] text-sm">
          CertifyIQ saves ${totalROI} across {employees.length} employees vs unguided exam prep.{" "}
          Guided pass rate: 89% vs unguided: 58%.{" "}
          Includes reduced retake costs + productivity recovery.
        </p>
      </div>

      {/* Full team table */}
      <div className="bg-[#0d1117] border border-[#21262d] rounded-lg overflow-hidden mb-6">
        <div className="px-5 py-3 border-b border-[#21262d]">
          <p className="text-[#f0f6fc] text-sm font-semibold">All Employees</p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-[#21262d]">
                {["Name", "Role", "Cert", "Score", "Verdict", "Weeks", "Meetings/wk", "Percentile", "ROI", "Action"].map((h) => (
                  <th key={h} className="text-left px-4 py-2.5 text-[#6e7681] uppercase tracking-widest font-medium text-[10px]">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {employees.map((emp) => {
                const verdict = VERDICTS[emp.id] || "APPROACHING";
                const style = getVerdictStyle(verdict);
                const isAtRisk = verdict === "NOT YET";
                return (
                  <tr
                    key={emp.id}
                    className="border-b border-[#21262d] hover:bg-[#161b22] transition-colors"
                    style={isAtRisk ? { borderLeft: "2px solid #da3633" } : {}}
                  >
                    <td className="px-4 py-3 text-[#f0f6fc] font-medium">{emp.name}</td>
                    <td className="px-4 py-3 text-[#8b949e]">{emp.role}</td>
                    <td className="px-4 py-3 font-mono text-[#8b949e]">{emp.certification_target}</td>
                    <td className="px-4 py-3 font-mono font-bold" style={{ color: getScoreColor(emp.current_practice_score) }}>
                      {emp.current_practice_score}%
                    </td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-0.5 rounded border font-medium text-[10px] ${style.text} ${style.bg} ${style.border}`}>
                        {verdict}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-mono text-[#8b949e]">{emp.weeks_until_exam}w</td>
                    <td className={`px-4 py-3 font-mono ${emp.meeting_hours_per_week > 22 ? "text-[#d29922]" : "text-[#8b949e]"}`}>
                      {emp.meeting_hours_per_week}h
                    </td>
                    <td className="px-4 py-3 font-mono text-[#8b949e]">P{PERCENTILES[emp.id] || 50}</td>
                    <td className="px-4 py-3 font-mono text-[#3fb950]">${ROI_PER_EMP[emp.id] || 0}</td>
                    <td className="px-4 py-3">
                      <a href={`/certify/${emp.id}`} className="text-[#1f6feb] hover:text-[#388bfd] transition-colors">
                        Analyze →
                      </a>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Intervention table */}
      {atRisk.length > 0 && (
        <div className="bg-[#0d1117] border border-[#da3633]/30 rounded-lg overflow-hidden mb-6">
          <div className="px-5 py-3 border-b border-[#da3633]/20">
            <p className="text-[#f85149] text-sm font-semibold">Intervention Required — {atRisk.length} employee{atRisk.length > 1 ? "s" : ""}</p>
          </div>
          <table className="w-full text-xs">
            <tbody>
              {atRisk.map((emp) => (
                <tr key={emp.id} className="border-b border-[#21262d] last:border-0">
                  <td className="px-4 py-3 text-[#f0f6fc] font-medium">{emp.name}</td>
                  <td className="px-4 py-3 font-mono text-[#8b949e]">{emp.certification_target}</td>
                  <td className="px-4 py-3 font-mono text-[#f85149]">{emp.current_practice_score}%</td>
                  <td className={`px-4 py-3 font-mono ${emp.meeting_hours_per_week > 22 ? "text-[#d29922]" : "text-[#8b949e]"}`}>
                    {emp.meeting_hours_per_week}h/wk meetings
                  </td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-0.5 border border-[#da3633]/50 text-[#f85149] bg-[#da3633]/10 rounded text-[10px]">
                      {VERDICTS[emp.id]}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <a href={`/certify/${emp.id}`} className="text-[#1f6feb] hover:text-[#388bfd] transition-colors">
                      Run Analysis →
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <a href="/" className="text-xs text-[#6e7681] hover:text-[#f0f6fc] transition-colors">
        ← Back to home
      </a>
    </div>
  );
}