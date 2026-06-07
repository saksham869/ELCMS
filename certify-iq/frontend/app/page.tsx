"use client";

import { useEffect, useState } from "react";
import {
  fetchEmployees,
  queryNaturalLanguage,
  getVerdictStyle,
  getAvatarColor,
  getInitials,
  getScoreColor,
  VERDICTS,
  PERCENTILES,
  ROI_PER_EMP,
  STATIC_EMPLOYEES,
  type Employee,
  type QueryResult,
} from "@/lib/api";

const EXAMPLE_QUERIES = [
  "Who is most at risk this month?",
  "What's our budget exposure?",
  "Which employee should take their exam soonest?",
];

const PRODUCT_CARDS = [
  {
    title: "Individual Analysis",
    label: "10-agent reasoning pipeline",
    href: "/certify/EMP-001",
    preview: [
      { w: "3/4", c: "#1f6feb" },
      { w: "1/2", c: "#21262d" },
      { w: "2/3", c: "#21262d" },
      { w: "3/4", c: "#238636" },
      { w: "1/2", c: "#21262d" },
    ],
  },
  {
    title: "Team Intelligence",
    label: "Manager readiness overview",
    href: "/dashboard",
    preview: [
      { w: "full", c: "#0d1117", chart: true },
      { w: "3/4", c: "#21262d" },
      { w: "1/2", c: "#21262d" },
    ],
  },
  {
    title: "ROI Calculation",
    label: "Business case builder",
    href: "/roi",
    preview: [
      { w: "1/2", c: "#21262d" },
      { w: "3/4", c: "#238636" },
      { w: "1/3", c: "#21262d" },
      { w: "2/3", c: "#21262d" },
    ],
  },
  {
    title: "Audit Trail",
    label: "Complete transparency log",
    href: "/audit",
    preview: [
      { w: "full", c: "#21262d" },
      { w: "full", c: "#0d1117" },
      { w: "full", c: "#0d1117" },
      { w: "full", c: "#0d1117" },
    ],
  },
];

const HOW_IT_WORKS = [
  {
    step: "01",
    title: "Predict",
    icon: (
      <svg className="w-5 h-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5">
        <path d="M2 14l6-6 4 4 6-8" strokeLinecap="round" strokeLinejoin="round" />
        <circle cx="16" cy="4" r="1.5" fill="currentColor" stroke="none" />
      </svg>
    ),
    text: "Readiness Forecaster calculates exam-ready date with confidence level, 6 weeks out.",
  },
  {
    step: "02",
    title: "Prevent",
    icon: (
      <svg className="w-5 h-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5">
        <path d="M10 3v4M10 13v4M3 10h4M13 10h4" strokeLinecap="round" />
        <circle cx="10" cy="10" r="3" />
      </svg>
    ),
    text: "Intervention Agent generates manager escalation with specific action plan before failure becomes inevitable.",
  },
  {
    step: "03",
    title: "Prove",
    icon: (
      <svg className="w-5 h-5" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5">
        <rect x="3" y="3" width="14" height="14" rx="2" />
        <path d="M7 10l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    text: "ROI Calculator quantifies the cost of doing nothing vs guided preparation, per employee and per team.",
  },
];

export default function Home() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [query, setQuery] = useState("");
  const [queryLoading, setQueryLoading] = useState(false);
  const [queryResult, setQueryResult] = useState<QueryResult | null>(null);
  const [queryError, setQueryError] = useState("");

  useEffect(() => {
    fetchEmployees()
      .then((d) => setEmployees(d.employees))
      .catch(() => setEmployees(STATIC_EMPLOYEES));
  }, []);

  const handleQuery = async (q?: string) => {
    const question = q ?? query;
    if (!question.trim()) return;
    setQuery(question);
    setQueryLoading(true);
    setQueryResult(null);
    setQueryError("");
    try {
      const result = await queryNaturalLanguage(question);
      setQueryResult(result);
    } catch {
      setQueryError("Unable to connect to backend. Start the server on port 8000.");
    } finally {
      setQueryLoading(false);
    }
  };

  return (
    <div>
      {/* ─── HERO ─── */}
      <section className="min-h-[calc(100vh-48px)] flex flex-col justify-center max-w-4xl mx-auto px-6 py-20">
        <p className="text-[#8b949e] text-xs tracking-widest uppercase mb-6">
          Microsoft Agents League 2026 · Reasoning Agents Track
        </p>

        <h1 className="text-[64px] font-bold leading-[1.05] text-[#f0f6fc] mb-6">
          Workforce AI Readiness
          <br />
          Intelligence.
        </h1>

        <p className="text-[#8b949e] text-lg max-w-lg mb-8 leading-relaxed">
          Companies invest millions in Azure.
          <br />
          CertifyIQ tells you if your team is certified to use what you bought —
          <br />
          6 weeks before the gap becomes a problem.
        </p>

        <div className="flex items-center gap-3 mb-10">
          <a
            href="#start"
            className="px-4 py-2 bg-[#1f6feb] hover:bg-[#388bfd] text-[#f0f6fc] text-sm font-medium rounded-md transition-colors"
          >
            Analyze your team →
          </a>
          <a
            href="/business"
            className="px-4 py-2 border border-[#30363d] text-[#8b949e] hover:text-[#f0f6fc] hover:border-[#8b949e] text-sm rounded-md transition-colors"
          >
            View business case
          </a>
        </div>

        <div className="flex items-center gap-4 text-[#6e7681] text-sm font-mono">
          <span>$5.5T skills gap</span>
          <span className="text-[#30363d]">|</span>
          <span>90% face shortages</span>
          <span className="text-[#30363d]">|</span>
          <span>$165 per exam attempt</span>
        </div>
      </section>

      {/* ─── PRODUCT PREVIEW ─── */}
      <section className="border-t border-[#21262d] py-20 px-6">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-[#f0f6fc] text-2xl font-bold mb-2">Four views. One truth.</h2>
          <p className="text-[#8b949e] text-sm mb-10">CertifyIQ surfaces what your data already knows.</p>

          <div className="grid grid-cols-2 gap-4">
            {PRODUCT_CARDS.map((card) => (
              <a
                key={card.href}
                href={card.href}
                className="border border-[#21262d] rounded-lg overflow-hidden hover:border-[#30363d] transition-colors group"
              >
                <div className="bg-[#0d1117] h-40 p-4 space-y-2 flex flex-col justify-center">
                  {card.preview.map((bar, i) =>
                    bar.chart ? (
                      <div key={i} className="flex items-end gap-1 h-16 mt-2">
                        {["AC", "JS", "ML", "RP"].map((n, j) => (
                          <div key={n} className="flex-1 flex flex-col items-center gap-1">
                            <div
                              className="w-full rounded-sm"
                              style={{
                                height: [62, 78, 45, 71][j] * 0.5 + "%",
                                background: ["#d29922","#3fb950","#f85149","#d29922"][j],
                                maxHeight: "100%",
                              }}
                            />
                            <span className="text-[6px] text-[#6e7681]">{n}</span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div
                        key={i}
                        className={`h-2 rounded-sm w-${bar.w}`}
                        style={{ background: bar.c, opacity: 0.6 + i * 0.1 }}
                      />
                    )
                  )}
                </div>
                <div className="px-4 py-3 border-t border-[#21262d]">
                  <p className="text-[#f0f6fc] text-sm font-medium group-hover:text-white transition-colors">
                    {card.title}
                  </p>
                  <p className="text-[#6e7681] text-xs mt-0.5">{card.label}</p>
                </div>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* ─── HOW IT WORKS ─── */}
      <section className="border-t border-[#21262d] py-20 px-6">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-[#f0f6fc] text-2xl font-bold mb-2">Predict. Prevent. Prove.</h2>
          <p className="text-[#8b949e] text-sm mb-12">Three actions. One pipeline. Zero guesswork.</p>

          <div className="grid grid-cols-3 gap-8">
            {HOW_IT_WORKS.map((item) => (
              <div key={item.step}>
                <div className="flex items-center gap-3 mb-4">
                  <span className="text-[#6e7681] text-xs font-mono">{item.step}</span>
                  <div className="text-[#8b949e]">{item.icon}</div>
                  <h3 className="text-[#f0f6fc] font-semibold">{item.title}</h3>
                </div>
                <p className="text-[#8b949e] text-sm leading-relaxed">{item.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── NL QUERY ─── */}
      <section className="border-t border-[#21262d] py-20 px-6">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-[#f0f6fc] text-2xl font-bold mb-2">Ask anything.</h2>
          <p className="text-[#8b949e] text-sm mb-8">
            Natural language query — powered by Foundry IQ knowledge grounding.
          </p>

          <div className="flex gap-2 mb-4">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleQuery()}
              placeholder="Who is most at risk this month?"
              className="flex-1 bg-[#0d1117] border border-[#21262d] text-[#f0f6fc] placeholder-[#6e7681] text-sm rounded-md px-4 py-2.5 focus:outline-none focus:border-[#1f6feb] font-mono transition-colors"
            />
            <button
              onClick={() => handleQuery()}
              disabled={queryLoading}
              className="px-4 py-2 bg-[#1f6feb] hover:bg-[#388bfd] disabled:opacity-50 text-[#f0f6fc] text-sm rounded-md transition-colors"
            >
              {queryLoading ? "..." : "Ask"}
            </button>
          </div>

          <div className="flex flex-wrap gap-2 mb-6">
            {EXAMPLE_QUERIES.map((q) => (
              <button
                key={q}
                onClick={() => handleQuery(q)}
                className="text-xs text-[#8b949e] border border-[#21262d] rounded-full px-3 py-1 hover:border-[#30363d] hover:text-[#f0f6fc] transition-colors"
              >
                {q}
              </button>
            ))}
          </div>

          {queryError && (
            <div className="bg-[#0d1117] border border-[#21262d] rounded-lg p-4 text-[#8b949e] text-sm">
              {queryError}
            </div>
          )}

          {queryResult && (
            <div className="bg-[#0d1117] border border-[#21262d] rounded-lg p-5 space-y-3">
              <p className="text-[#6e7681] text-xs font-mono">Q: {queryResult.question}</p>
              <p className="text-[#f0f6fc] text-sm leading-relaxed">{queryResult.answer}</p>
              {queryResult.action && (
                <p className="text-[#1f6feb] text-xs">→ {queryResult.action}</p>
              )}
              {queryResult.citations?.length > 0 && (
                <div className="flex flex-wrap gap-1 pt-1">
                  {queryResult.citations.map((c, i) => (
                    <span key={i} className="text-[10px] text-[#6e7681] bg-[#161b22] border border-[#30363d] rounded px-2 py-0.5">
                      {c}
                    </span>
                  ))}
                </div>
              )}
              <p className="text-[#6e7681] text-xs">
                Confidence: {((queryResult.confidence || 0) * 100).toFixed(0)}%
              </p>
            </div>
          )}
        </div>
      </section>

      {/* ─── EMPLOYEE GRID ─── */}
      <section id="start" className="border-t border-[#21262d] py-20 px-6">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-[#f0f6fc] text-2xl font-bold mb-2">Start here.</h2>
          <p className="text-[#8b949e] text-sm mb-8">Select an employee to run the analysis.</p>

          <div className="grid grid-cols-2 gap-4">
            {(employees.length > 0 ? employees : STATIC_EMPLOYEES).map((emp) => {
              const verdict = VERDICTS[emp.id] || "APPROACHING";
              const percentile = PERCENTILES[emp.id] || 50;
              const roi = ROI_PER_EMP[emp.id] || 150;
              const style = getVerdictStyle(verdict);
              const avatarBg = getAvatarColor(verdict);
              const scoreColor = getScoreColor(emp.current_practice_score);
              const progress = Math.round((emp.current_practice_score / 75) * 100);

              return (
                <a
                  key={emp.id}
                  href={`/certify/${emp.id}`}
                  className="block border border-[#21262d] hover:border-[#30363d] rounded-lg p-5 transition-colors bg-[#0d1117] group"
                >
                  {/* Row 1: Avatar + name + score */}
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div
                        className={`w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold text-white ${avatarBg}`}
                      >
                        {getInitials(emp.name)}
                      </div>
                      <div>
                        <p className="text-[#f0f6fc] text-sm font-semibold group-hover:text-white">{emp.name}</p>
                        <p className="text-[#8b949e] text-xs">{emp.role}</p>
                        <p className="text-[#6e7681] text-xs">{emp.certification_target}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="text-xl font-bold font-mono" style={{ color: scoreColor }}>
                        {emp.current_practice_score}
                      </span>
                      <p className="text-[#6e7681] text-xs">/ 75 pass</p>
                    </div>
                  </div>

                  {/* Score bar */}
                  <div className="h-0.5 bg-[#21262d] rounded-full mb-3 overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all"
                      style={{ width: `${Math.min(progress, 100)}%`, background: scoreColor }}
                    />
                  </div>

                  {/* Row 2: verdict + percentile + roi */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className={`text-xs px-2 py-0.5 rounded border font-medium ${style.text} ${style.bg} ${style.border}`}>
                        {verdict}
                      </span>
                      <span className="text-xs text-[#6e7681]">
                        {emp.weeks_until_exam}w to exam
                      </span>
                    </div>
                    <div className="flex items-center gap-2 text-xs text-[#6e7681]">
                      <span>P{percentile}</span>
                      <span className="text-[#3fb950]">${roi} ROI</span>
                    </div>
                  </div>

                  <div className="mt-3 pt-3 border-t border-[#21262d]">
                    <span className="text-xs text-[#1f6feb] group-hover:text-[#388bfd] transition-colors">
                      Run Analysis →
                    </span>
                  </div>
                </a>
              );
            })}
          </div>

          {/* Bottom links */}
          <div className="flex gap-6 mt-10 pt-8 border-t border-[#21262d]">
            <a href="/dashboard" className="text-sm text-[#8b949e] hover:text-[#f0f6fc] transition-colors">
              Manager Dashboard →
            </a>
            <a href="/roi" className="text-sm text-[#8b949e] hover:text-[#f0f6fc] transition-colors">
              ROI Calculator →
            </a>
            <a href="/audit" className="text-sm text-[#8b949e] hover:text-[#f0f6fc] transition-colors">
              Audit Trail →
            </a>
            <a href="/business" className="text-sm text-[#8b949e] hover:text-[#f0f6fc] transition-colors">
              Business Case →
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}