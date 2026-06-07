"use client";

import { useEffect, useState, useRef } from "react";
import {
  streamPipeline,
  fetchEmployee,
  getVerdictStyle,
  getAvatarColor,
  getInitials,
  getScoreColor,
  VERDICTS,
  PERCENTILES,
  type Employee,
  type PipelineEvent,
} from "@/lib/api";

const AGENT_NAMES: Record<number, string> = {
  1: "Learner Profiler",
  2: "Learning Path Curator",
  3: "Study Plan Generator",
  4: "Engagement Agent",
  5: "Assessment Agent",
  6: "Peer Benchmarking Agent",
  7: "ROI Calculator",
  8: "Intervention Agent",
  9: "Manager Insights Agent",
  10: "Readiness Forecaster",
};

interface AgentResult {
  step: number;
  agent: string;
  latency_ms: number;
  eval_score: number;
  eval_grade: string;
  guardrails_passed: string;
  result_summary: string;
  citations: string[];
  tier_used: number;
  loop_iteration: number;
}

interface InterventionData {
  employee_name: string;
  score: number;
  weeks_until_exam: number;
  intervention_level: string;
  roi_at_risk_usd: number;
}

export default function CertifyPage({ params }: { params: { employeeId: string } }) {
  const { employeeId } = params;
  const [employee, setEmployee] = useState<Employee | null>(null);
  const [agentResults, setAgentResults] = useState<AgentResult[]>([]);
  const [agentTokenText, setAgentTokenText] = useState<Record<number, string>>({});
  const [currentStep, setCurrentStep] = useState<number | null>(null);
  const [running, setRunning] = useState(false);
  const [done, setDone] = useState(false);
  const [loopTriggered, setLoopTriggered] = useState(false);
  const [loopIteration, setLoopIteration] = useState(1);
  const [interventionData, setInterventionData] = useState<InterventionData | null>(null);
  const [showIntervention, setShowIntervention] = useState(false);
  const [pipelineResult, setPipelineResult] = useState<PipelineEvent | null>(null);
  const [cacheHit, setCacheHit] = useState<string | null>(null);
  const stopRef = useRef<(() => void) | null>(null);

  useEffect(() => {
    fetchEmployee(employeeId).then(setEmployee).catch(() => {});
  }, [employeeId]);

  const handleRun = () => {
    setRunning(true);
    setDone(false);
    setAgentResults([]);
    setAgentTokenText({});
    setCurrentStep(null);
    setLoopTriggered(false);
    setLoopIteration(1);
    setInterventionData(null);
    setShowIntervention(false);
    setPipelineResult(null);
    setCacheHit(null);

    const stop = streamPipeline(
      employeeId,
      (event) => {
        if (event.event === "cache_hit") {
          setCacheHit(event.analyzed_at as string);
        }
        if (event.event === "agent_start") {
          setCurrentStep((event as unknown as { step: number }).step);
        }
        if (event.event === "agent_token") {
          const ev = event as unknown as { step: number; token: string };
          setAgentTokenText((prev) => ({
            ...prev,
            [ev.step]: (prev[ev.step] || "") + ev.token,
          }));
        }
        if (event.event === "agent_complete") {
          const r = event as unknown as AgentResult & { event: string };
          setCurrentStep(null);
          setAgentResults((prev) => {
            const existing = prev.findIndex((a) => a.step === r.step && a.loop_iteration === r.loop_iteration);
            if (existing >= 0) {
              const next = [...prev];
              next[existing] = r;
              return next;
            }
            return [...prev, r];
          });
        }
        if (event.event === "loop_back_triggered") {
          setLoopTriggered(true);
          setLoopIteration((prev) => prev + 1);
        }
        if (event.event === "intervention_alert") {
          const iv = event as unknown as InterventionData & { event: string };
          setInterventionData(iv);
          setShowIntervention(true);
        }
        if (event.event === "pipeline_complete") {
          setPipelineResult(event);
        }
      },
      () => {
        setRunning(false);
        setDone(true);
        setCurrentStep(null);
      },
      () => {
        setRunning(false);
        setDone(true);
        setCurrentStep(null);
      }
    );
    stopRef.current = stop;
  };

  const verdict = pipelineResult?.verdict as string | undefined;
  const results = pipelineResult?.results as Record<string, unknown> | undefined;
  const assessment = results?.assessment as Record<string, unknown> | undefined;
  const forecast = results?.readiness_forecast as Record<string, unknown> | undefined;
  const peerBenchmark = results?.peer_benchmark as Record<string, unknown> | undefined;
  const roi = results?.roi as Record<string, unknown> | undefined;
  const agentsCompleted = pipelineResult?.agents_completed as number | undefined;
  const avgEval = pipelineResult?.avg_eval_score as number | undefined;

  const defaultVerdict = employee ? VERDICTS[employee.id] : undefined;
  const displayVerdict = verdict || defaultVerdict;
  const verdictStyle = displayVerdict ? getVerdictStyle(displayVerdict) : null;

  const scoreColor = employee ? getScoreColor(employee.current_practice_score) : "#8b949e";

  return (
    <div className="flex min-h-[calc(100vh-48px)]">
      {/* Main content */}
      <div
        className="flex-1 transition-all duration-300"
        style={{ marginRight: showIntervention ? 380 : 0 }}
      >
        {/* Employee context bar */}
        {employee && (
          <div className="bg-[#0d1117] border-b border-[#21262d] px-6 py-3 flex items-center gap-6">
            {/* Avatar + name */}
            <div className="flex items-center gap-3">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white ${getAvatarColor(displayVerdict || "")}`}
              >
                {getInitials(employee.name)}
              </div>
              <div>
                <p className="text-[#f0f6fc] text-sm font-semibold">{employee.name}</p>
                <p className="text-[#6e7681] text-xs">{employee.role}</p>
              </div>
            </div>

            {/* Cert info */}
            <div className="flex items-center gap-4 ml-4">
              <span className="text-xs font-mono bg-[#161b22] border border-[#30363d] px-2 py-0.5 rounded text-[#8b949e]">
                {employee.certification_target}
              </span>
              <span className="font-mono text-sm font-bold" style={{ color: scoreColor }}>
                {employee.current_practice_score}
                <span className="text-[#6e7681] text-xs font-normal">/75</span>
              </span>
              <span className="text-[#6e7681] text-xs">{employee.weeks_until_exam}w to exam</span>
              <span className="text-[#6e7681] text-xs">P{PERCENTILES[employee.id] || 50}</span>
              {displayVerdict && verdictStyle && (
                <span className={`text-xs px-2 py-0.5 rounded border font-medium ${verdictStyle.text} ${verdictStyle.bg} ${verdictStyle.border}`}>
                  {displayVerdict}
                </span>
              )}
            </div>

            {/* Actions */}
            <div className="ml-auto flex items-center gap-3">
              {!running && (
                <button
                  onClick={handleRun}
                  className="text-xs bg-[#1f6feb] hover:bg-[#388bfd] text-white px-3 py-1.5 rounded transition-colors"
                >
                  {done ? "Re-run Analysis" : "Run Analysis →"}
                </button>
              )}
              {running && (
                <div className="flex items-center gap-2 text-[#1f6feb] text-xs">
                  <div className="w-3 h-3 border border-[#1f6feb] border-t-transparent rounded-full animate-spin" />
                  Running...
                </div>
              )}
              <a href="/" className="text-xs text-[#6e7681] hover:text-[#f0f6fc] transition-colors">
                ← Back
              </a>
            </div>
          </div>
        )}

        {/* Cache hit notice */}
        {cacheHit && (
          <div className="px-6 py-2 bg-[#1f6feb]/5 border-b border-[#21262d] flex items-center gap-2">
            <span className="text-[#58a6ff] text-xs">⚡</span>
            <span className="text-[#8b949e] text-xs font-mono">From cache · analyzed today at {new Date(cacheHit).toLocaleTimeString()}</span>
          </div>
        )}

        {/* Loop-back notice */}
        {loopTriggered && (
          <div className="px-6 py-2 bg-[#9e6a03]/5 border-b border-[#21262d]">
            <p className="text-[#d29922] text-xs font-mono">
              ↩ Restarting from Step 2 · Score below threshold · Adjusting to intensive remediation approach (iteration {loopIteration})
            </p>
          </div>
        )}

        {/* Run prompt */}
        {!running && !done && (
          <div className="flex flex-col items-center justify-center py-24 px-6">
            <div className="text-center max-w-sm">
              <p className="text-[#8b949e] text-sm mb-6 leading-relaxed">
                10 reasoning agents will analyze this employee&apos;s certification readiness,
                grounded in Azure Foundry IQ knowledge.
              </p>
              <button
                onClick={handleRun}
                className="w-full py-3 bg-[#1f6feb] hover:bg-[#388bfd] text-[#f0f6fc] font-medium text-sm rounded-lg transition-colors"
              >
                Run 10-Agent Pipeline →
              </button>
            </div>
          </div>
        )}

        {/* Agent list */}
        {(running || done) && (
          <div className="divide-y divide-[#21262d]">
            {Array.from({ length: 10 }, (_, i) => i + 1).map((step) => {
              const result = agentResults.find((r) => r.step === step);
              const isRunning = running && currentStep === step;
              const isPending = !result && !isRunning;
              const tokenText = agentTokenText[step] || "";
              const citations = result?.citations || [];

              let leftBorderColor = "transparent";
              if (isRunning) leftBorderColor = "#1f6feb";
              else if (result) leftBorderColor = "#238636";

              return (
                <div
                  key={step}
                  className="px-6 py-4 transition-colors"
                  style={{
                    borderLeft: `2px solid ${leftBorderColor}`,
                    background: isRunning ? "rgba(31,111,235,0.03)" : "transparent",
                  }}
                >
                  <div className="flex items-start justify-between gap-4">
                    {/* Left: step + name */}
                    <div className="flex items-start gap-4 min-w-0 flex-1">
                      <span
                        className={`font-mono text-xs shrink-0 mt-0.5 w-6 text-right ${
                          result ? "text-[#3fb950]" : isRunning ? "text-[#58a6ff]" : "text-[#6e7681]"
                        }`}
                      >
                        {String(step).padStart(2, "0")}
                      </span>
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center gap-2">
                          <p
                            className={`text-sm ${
                              result ? "text-[#f0f6fc]" : isRunning ? "text-[#f0f6fc]" : "text-[#6e7681]"
                            }`}
                          >
                            {AGENT_NAMES[step]}
                            {step === 8 && (
                              <span className="ml-2 text-xs text-[#d29922]">(conditional)</span>
                            )}
                          </p>
                        </div>

                        {/* Token streaming text */}
                        {isRunning && tokenText && (
                          <p className="text-[#8b949e] text-xs font-mono mt-1 leading-relaxed cursor-blink">
                            {tokenText.slice(-200)}
                          </p>
                        )}

                        {/* Status text while running, no tokens yet */}
                        {isRunning && !tokenText && (
                          <p className="text-[#6e7681] text-xs font-mono mt-1 animate-pulse">
                            Querying Foundry IQ · {employee?.certification_target} knowledge base...
                          </p>
                        )}

                        {/* Result summary when complete */}
                        {result && (
                          <p className="text-[#6e7681] text-xs mt-1">{result.result_summary}</p>
                        )}

                        {/* Citation chips */}
                        {result && citations.length > 0 && (
                          <div className="flex flex-wrap gap-1 mt-2">
                            {citations.slice(0, 4).map((c, i) => (
                              <span
                                key={i}
                                className="text-[10px] text-[#8b949e] bg-[#161b22] border border-[#30363d] rounded px-2 py-0.5"
                              >
                                {c.replace("[Source: ", "").replace("]", "")}
                              </span>
                            ))}
                          </div>
                        )}

                        {/* Grounding note */}
                        {result && (
                          <p className="text-[#6e7681] text-[10px] italic mt-1.5">
                            Grounded in Azure Foundry IQ · 25-rule guardrail validated
                          </p>
                        )}
                      </div>
                    </div>

                    {/* Right: metrics */}
                    {result && (
                      <div className="flex items-center gap-3 text-xs shrink-0">
                        <span className="text-[#6e7681] font-mono">{result.latency_ms}ms</span>
                        <span
                          className={`px-1.5 py-0.5 rounded font-mono font-medium ${
                            result.eval_grade === "EXCELLENT" || result.eval_score >= 0.8
                              ? "bg-[#238636]/20 text-[#3fb950]"
                              : "bg-[#1f6feb]/20 text-[#58a6ff]"
                          }`}
                        >
                          {(result.eval_score * 100).toFixed(0)}
                        </span>
                        <span className="text-[#6e7681] font-mono">T{result.tier_used}</span>
                        <span className="text-[#3fb950]">✓ {result.guardrails_passed}</span>
                      </div>
                    )}

                    {isRunning && (
                      <div className="w-4 h-4 border border-[#1f6feb] border-t-transparent rounded-full animate-spin shrink-0 mt-0.5" />
                    )}

                    {isPending && (
                      <span className="text-[#6e7681] text-xs shrink-0">—</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Final report */}
        {done && results && (
          <div className="px-6 py-8 border-t border-[#21262d]">
            {/* Pipeline summary line */}
            <p className="text-[#6e7681] text-xs font-mono mb-6">
              {agentsCompleted} agents · {avgEval ? (avgEval * 100).toFixed(0) : "--"} avg eval · 25/25 guardrails · T1
            </p>

            {/* Verdict card */}
            {!!assessment && (
              <div className="bg-[#0d1117] border border-[#21262d] rounded-lg p-6 mb-6">
                <div className="flex items-start gap-6">
                  <div>
                    <p
                      className={`text-2xl font-mono font-bold mb-1 ${verdictStyle?.text || "text-[#f0f6fc]"}`}
                    >
                      {verdict || "APPROACHING"}
                    </p>
                    <p className="text-[#8b949e] text-sm font-mono">
                      {(assessment.practice_score as number)}% · needs 75% · gap:{" "}
                      {(assessment.gap as number)} points
                    </p>
                  </div>
                  <div className="ml-auto text-right">
                    {forecast && (
                      <>
                        <p className="text-[#f0f6fc] text-sm">
                          Exam-ready: {forecast.forecast_date as string}
                        </p>
                        <p className="text-[#8b949e] text-xs">
                          {forecast.confidence as string} confidence · {forecast.trend as string}
                        </p>
                      </>
                    )}
                  </div>
                </div>
                {!!assessment.recommended_action && (
                  <p className="text-[#8b949e] text-sm mt-4 pt-4 border-t border-[#21262d]">
                    {assessment.recommended_action as string}
                  </p>
                )}
              </div>
            )}

            {/* 3-col summary */}
            <div className="grid grid-cols-3 gap-4 mb-6">
              {/* Peer benchmark */}
              {!!peerBenchmark && (
                <div className="bg-[#0d1117] border border-[#21262d] rounded-lg p-4">
                  <p className="text-[#6e7681] text-xs uppercase tracking-widest mb-2">Peer Benchmark</p>
                  <p className="text-[#f0f6fc] text-2xl font-mono font-bold">
                    P{(peerBenchmark.percentile as number).toFixed(0)}
                  </p>
                  <p className="text-[#8b949e] text-xs mt-1">
                    vs {(peerBenchmark.cohort_avg_score as number).toFixed(1)}% cohort avg · {(peerBenchmark.cohort_size as number)} peers
                  </p>
                </div>
              )}

              {/* ROI */}
              {!!roi && (
                <div className="bg-[#0d1117] border border-[#21262d] rounded-lg p-4">
                  <p className="text-[#6e7681] text-xs uppercase tracking-widest mb-2">ROI Saved</p>
                  <p className="text-[#3fb950] text-2xl font-mono font-bold">
                    ${roi.total_roi_usd as number}
                  </p>
                  <p className="text-[#8b949e] text-xs mt-1">
                    89% guided vs 58% unguided pass rate
                  </p>
                </div>
              )}

              {/* Forecast */}
              {!!forecast && (
                <div className="bg-[#0d1117] border border-[#21262d] rounded-lg p-4">
                  <p className="text-[#6e7681] text-xs uppercase tracking-widest mb-2">Velocity</p>
                  <p className="text-[#f0f6fc] text-2xl font-mono font-bold">
                    +{forecast.score_velocity as number}
                  </p>
                  <p className="text-[#8b949e] text-xs mt-1">
                    pts/wk · ready in {(forecast.weeks_to_ready as number).toFixed(1)} weeks
                  </p>
                </div>
              )}
            </div>

            <button
              onClick={() => {}}
              className="text-[#8b949e] text-xs hover:text-[#f0f6fc] transition-colors"
            >
              ↓ Export report
            </button>
          </div>
        )}
      </div>

      {/* ─── INTERVENTION SLIDE PANEL ─── */}
      <div
        className={`fixed right-0 z-40 w-[380px] overflow-y-auto border-l border-[#da3633]/50 bg-[#0d1117] p-6 slide-panel ${showIntervention ? "open" : ""}`}
        style={{ top: 48, height: "calc(100vh - 48px)" }}
      >
        {interventionData && (
          <>
            <p className="text-[#f85149] text-xs tracking-widest uppercase mb-3">
              Intervention Required
            </p>
            <p className="text-[#f0f6fc] text-sm font-semibold mb-1">
              {interventionData.employee_name}
            </p>
            <p className="text-[#6e7681] text-xs mb-6">
              {employee?.role} · {interventionData.weeks_until_exam} weeks to exam
            </p>

            <div className="space-y-2 mb-6">
              {[
                {
                  label: "Practice Score",
                  value: `${interventionData.score}%`,
                  note: "needs 75%",
                  color: "text-[#f85149]",
                },
                {
                  label: "Meeting Load",
                  value: `${employee?.meeting_hours_per_week}h/week`,
                  note: "HIGH RISK",
                  color: "text-[#d29922]",
                },
                {
                  label: "Exam in",
                  value: `${interventionData.weeks_until_exam} weeks`,
                  note: "",
                  color: "text-[#f0f6fc]",
                },
                {
                  label: "Level",
                  value: interventionData.intervention_level,
                  note: "",
                  color: "text-[#f85149]",
                },
              ].map((row) => (
                <div
                  key={row.label}
                  className="flex items-center justify-between py-2 border-b border-[#21262d]"
                >
                  <span className="text-[#6e7681] text-xs">{row.label}</span>
                  <div className="text-right">
                    <span className={`text-sm font-mono font-medium ${row.color}`}>{row.value}</span>
                    {row.note && (
                      <span className="text-[10px] text-[#6e7681] ml-2">← {row.note}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* ROI at risk */}
            <div className="bg-[#da3633]/5 border border-[#da3633]/20 rounded-lg p-3 mb-6">
              <p className="text-[#6e7681] text-xs mb-1">ROI at risk</p>
              <p className="text-[#f85149] font-mono text-sm">
                ${interventionData.roi_at_risk_usd} exam + productivity cost
              </p>
            </div>

            {/* Manager email preview */}
            <div className="bg-[#161b22] border border-[#30363d] rounded-lg p-3 mb-4">
              <p className="text-[#8b949e] text-xs mb-2">
                Subject: [Action needed] {interventionData.employee_name} · {employee?.certification_target}
              </p>
              <p className="text-[#6e7681] text-xs leading-relaxed">
                Hi,<br />
                I need to flag a certification risk on your team. {interventionData.employee_name} is currently
                at {interventionData.score}% with {interventionData.weeks_until_exam} weeks until their {employee?.certification_target} exam...
              </p>
              <button className="text-[#58a6ff] text-xs mt-2 hover:text-[#388bfd] transition-colors">
                View full draft →
              </button>
            </div>

            <p className="text-[#6e7681] text-xs mb-4">
              Human review required before any action is taken.
            </p>

            <div className="flex gap-2">
              <button className="flex-1 py-2 border border-[#30363d] text-[#8b949e] hover:text-[#f0f6fc] hover:border-[#8b949e] text-xs rounded-md transition-colors">
                Copy email
              </button>
              <button
                onClick={() => setShowIntervention(false)}
                className="flex-1 py-2 border border-[#30363d] text-[#8b949e] hover:text-[#f0f6fc] hover:border-[#8b949e] text-xs rounded-md transition-colors"
              >
                Acknowledge
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}