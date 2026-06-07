"use client";

import { useEffect, useState, useRef } from "react";
import { streamPipeline, fetchEmployee, getVerdictColor, getScoreColor, type Employee, type PipelineEvent } from "@/lib/api";

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

export default function CertifyPage({ params }: { params: { employeeId: string } }) {
  const { employeeId } = params;
  const [employee, setEmployee] = useState<Employee | null>(null);
  const [events, setEvents] = useState<PipelineEvent[]>([]);
  const [agentResults, setAgentResults] = useState<AgentResult[]>([]);
  const [running, setRunning] = useState(false);
  const [done, setDone] = useState(false);
  const [loopTriggered, setLoopTriggered] = useState(false);
  const [interventionAlert, setInterventionAlert] = useState<PipelineEvent | null>(null);
  const [showIntervention, setShowIntervention] = useState(false);
  const [pipelineResult, setPipelineResult] = useState<PipelineEvent | null>(null);
  const stopRef = useRef<(() => void) | null>(null);

  useEffect(() => {
    fetchEmployee(employeeId).then(setEmployee).catch(() => {});
  }, [employeeId]);

  const handleRun = () => {
    setRunning(true);
    setDone(false);
    setEvents([]);
    setAgentResults([]);
    setLoopTriggered(false);
    setInterventionAlert(null);
    setShowIntervention(false);
    setPipelineResult(null);

    const stop = streamPipeline(
      employeeId,
      (event) => {
        setEvents((prev) => [...prev, event]);

        if (event.event === "agent_complete") {
          const r = event as unknown as AgentResult & { event: string };
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
        }

        if (event.event === "intervention_alert") {
          setInterventionAlert(event);
          setShowIntervention(true);
        }

        if (event.event === "pipeline_complete") {
          setPipelineResult(event);
        }
      },
      () => {
        setRunning(false);
        setDone(true);
      },
      (err) => {
        console.error(err);
        setRunning(false);
        setDone(true);
      }
    );
    stopRef.current = stop;
  };

  const verdict = pipelineResult?.verdict as string | undefined;
  const results = pipelineResult?.results as Record<string, unknown> | undefined;

  return (
    <div className="max-w-6xl mx-auto px-6 py-8">
      {/* Employee Bar */}
      {employee && (
        <div className="bg-[#0d1429] border border-white/10 rounded-2xl p-5 mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">{employee.name}</h1>
            <p className="text-gray-400">
              {employee.role} · {employee.certification_target} · {employee.weeks_until_exam} weeks to exam
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div
              className="w-16 h-16 rounded-full border-4 flex items-center justify-center text-xl font-bold"
              style={{
                borderColor: getScoreColor(employee.current_practice_score),
                color: getScoreColor(employee.current_practice_score),
              }}
            >
              {employee.current_practice_score}
            </div>
            {verdict && (
              <span className={`px-3 py-1 rounded-lg border text-sm font-semibold ${getVerdictColor(verdict)}`}>
                {verdict}
              </span>
            )}
          </div>
        </div>
      )}

      {/* Loop-back Banner */}
      {loopTriggered && (
        <div className="bg-orange-500/10 border border-orange-500/30 rounded-xl p-4 mb-4 flex items-center gap-3">
          <span className="text-orange-400 text-lg">↩</span>
          <p className="text-orange-300 text-sm font-medium">
            Loop-back triggered: Assessment returned NOT YET — re-running with intensive remediation plan
          </p>
        </div>
      )}

      {/* Run Button */}
      {!running && !done && (
        <button
          onClick={handleRun}
          className="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-bold text-lg rounded-2xl transition-all mb-6"
        >
          Run 10-Agent CertifyIQ Pipeline
        </button>
      )}

      {running && (
        <div className="flex items-center gap-3 text-blue-300 mb-6">
          <div className="w-4 h-4 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
          <span className="text-sm">Pipeline running — streaming agent results...</span>
        </div>
      )}

      {/* Agent Pipeline Display */}
      <div className="grid grid-cols-1 gap-3 mb-6">
        {Array.from({ length: 10 }, (_, i) => i + 1).map((step) => {
          const result = agentResults.find((r) => r.step === step);
          const isRunning =
            running &&
            events.some((e) => e.event === "agent_start" && (e as unknown as { step: number }).step === step) &&
            !result;

          return (
            <div
              key={step}
              className={`border rounded-xl p-4 transition-all ${
                result
                  ? "bg-[#0d1429] border-white/10"
                  : isRunning
                  ? "bg-blue-500/5 border-blue-500/30"
                  : "bg-[#0a0f1e] border-white/5"
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span
                    className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
                      result
                        ? "bg-green-500/20 text-green-400"
                        : isRunning
                        ? "bg-blue-500/20 text-blue-400"
                        : "bg-white/5 text-gray-600"
                    }`}
                  >
                    {step === 8 ? "!" : step}
                  </span>
                  <div>
                    <p className={`font-medium text-sm ${result ? "text-white" : "text-gray-600"}`}>
                      {AGENT_NAMES[step]}
                      {step === 8 && <span className="ml-2 text-xs text-orange-400">(conditional)</span>}
                    </p>
                    {result && (
                      <p className="text-xs text-gray-500 mt-0.5">{result.result_summary}</p>
                    )}
                  </div>
                </div>
                {result && (
                  <div className="flex items-center gap-3 text-xs">
                    <span className="text-gray-500">{result.latency_ms}ms</span>
                    <span
                      className={`px-2 py-0.5 rounded font-medium ${
                        result.eval_grade === "EXCELLENT"
                          ? "bg-green-500/20 text-green-400"
                          : "bg-blue-500/20 text-blue-400"
                      }`}
                    >
                      {(result.eval_score * 100).toFixed(0)}
                    </span>
                    <span className="text-gray-600">T{result.tier_used}</span>
                    <span className="text-green-500">✓ {result.guardrails_passed}</span>
                  </div>
                )}
                {isRunning && (
                  <div className="w-4 h-4 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Final Report */}
      {done && results && (
        <div className="space-y-6">
          <h2 className="text-xl font-bold text-white">Pipeline Complete — Final Report</h2>

          {/* Assessment */}
          {!!results.assessment && (
            <div className="bg-[#0d1429] border border-white/10 rounded-2xl p-6">
              <h3 className="font-semibold text-white mb-3">Assessment Verdict</h3>
              <div className="flex items-center gap-4">
                <span
                  className={`text-2xl font-bold px-4 py-2 rounded-xl border ${getVerdictColor(verdict || "")}`}
                >
                  {verdict}
                </span>
                <div>
                  <p className="text-gray-300">
                    Score: {(results.assessment as Record<string, unknown>).practice_score as number}% / 75% threshold
                  </p>
                  <p className="text-sm text-gray-500">
                    {(results.assessment as Record<string, unknown>).recommended_action as string}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Peer Benchmark */}
          {!!results.peer_benchmark && (
            <div className="bg-[#0d1429] border border-white/10 rounded-2xl p-6">
              <h3 className="font-semibold text-white mb-3">Peer Benchmarking</h3>
              <p className="text-teal-300 text-sm">
                {(results.peer_benchmark as Record<string, unknown>).benchmark_insight as string}
              </p>
            </div>
          )}

          {/* ROI */}
          {!!results.roi && (
            <div className="bg-[#0d1429] border border-white/10 rounded-2xl p-6">
              <h3 className="font-semibold text-white mb-3">ROI Analysis</h3>
              <p className="text-green-300 text-sm">
                {(results.roi as Record<string, unknown>).roi_message as string}
              </p>
            </div>
          )}

          {/* Readiness Forecast */}
          {!!results.readiness_forecast && (
            <div className="bg-[#0d1429] border border-white/10 rounded-2xl p-6">
              <h3 className="font-semibold text-white mb-3">Readiness Forecast</h3>
              <p className="text-blue-300 text-sm">
                {(results.readiness_forecast as Record<string, unknown>).forecast_message as string}
              </p>
            </div>
          )}

          <a
            href="/"
            className="inline-block mt-4 text-sm text-gray-400 hover:text-white transition-colors"
          >
            ← Back to employees
          </a>
        </div>
      )}

      {/* Intervention Modal */}
      {showIntervention && interventionAlert && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-6">
          <div className="bg-[#1a0a0a] border-2 border-red-500/50 rounded-2xl max-w-lg w-full p-8">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 bg-red-500/20 rounded-full flex items-center justify-center text-red-400 text-xl">
                !
              </div>
              <div>
                <h2 className="text-red-400 font-bold text-lg">Intervention Alert</h2>
                <p className="text-gray-500 text-sm">CertifyIQ AI Pipeline</p>
              </div>
            </div>
            <p className="text-white font-medium mb-2">
              {interventionAlert.employee_name as string} requires immediate support
            </p>
            <div className="grid grid-cols-2 gap-3 mb-4 text-sm">
              <div className="bg-red-500/10 rounded-lg p-3">
                <p className="text-gray-400">Practice Score</p>
                <p className="text-red-300 font-bold">{interventionAlert.score as number}%</p>
              </div>
              <div className="bg-orange-500/10 rounded-lg p-3">
                <p className="text-gray-400">Weeks Until Exam</p>
                <p className="text-orange-300 font-bold">{interventionAlert.weeks_until_exam as number}</p>
              </div>
              <div className="bg-yellow-500/10 rounded-lg p-3">
                <p className="text-gray-400">Intervention Level</p>
                <p className="text-yellow-300 font-bold">{interventionAlert.intervention_level as string}</p>
              </div>
              <div className="bg-green-500/10 rounded-lg p-3">
                <p className="text-gray-400">ROI at Risk</p>
                <p className="text-green-300 font-bold">${interventionAlert.roi_at_risk_usd as number}</p>
              </div>
            </div>
            <p className="text-xs text-gray-500 mb-4">
              Manager email draft has been generated. Human review required before any action.
            </p>
            <button
              onClick={() => setShowIntervention(false)}
              className="w-full py-2.5 bg-red-600 hover:bg-red-500 text-white font-medium rounded-xl transition-colors"
            >
              Acknowledge & Continue
            </button>
          </div>
        </div>
      )}
    </div>
  );
}