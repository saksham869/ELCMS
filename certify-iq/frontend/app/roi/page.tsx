"use client";

import { useState } from "react";

export default function ROIPage() {
  const [teamSize, setTeamSize] = useState(10);
  const [examCost, setExamCost] = useState(165);
  const [guidedRate, setGuidedRate] = useState(89);
  const [unguidedRate, setUnguidedRate] = useState(58);
  const [studyWeeks, setStudyWeeks] = useState(6);

  const guided = guidedRate / 100;
  const unguided = unguidedRate / 100;
  const unguidedAttempts = 1 / unguided;
  const guidedAttempts = 1 / guided;
  const unguidedCost = unguidedAttempts * examCost;
  const guidedCost = guidedAttempts * examCost;
  const costSavingsPerEmp = unguidedCost - guidedCost;
  const productivityPerEmp = studyWeeks * 200 * 0.3;
  const totalPerEmp = costSavingsPerEmp + productivityPerEmp;
  const totalROI = totalPerEmp * teamSize;

  const yr1 = totalROI;
  const yr3 = totalROI * 3.2;
  const yr5 = totalROI * 5.8;

  const INPUT_CLASS =
    "w-full bg-[#0d1117] border border-[#21262d] text-[#f0f6fc] font-mono text-sm rounded px-3 py-2 focus:outline-none focus:border-[#1f6feb] transition-colors";

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      <div className="mb-8">
        <h1 className="text-[#f0f6fc] text-2xl font-bold">ROI Calculator</h1>
        <p className="text-[#6e7681] text-sm mt-1">
          Calculate the financial impact of CertifyIQ-guided vs unguided exam preparation
        </p>
      </div>

      <div className="grid grid-cols-2 gap-8">
        {/* Inputs */}
        <div>
          <p className="text-[#6e7681] text-xs uppercase tracking-widest mb-5">Configure your scenario</p>

          <div className="space-y-4">
            {[
              { label: "Team size", value: teamSize, set: setTeamSize, min: 1, max: 1000 },
              { label: "Exam cost (USD)", value: examCost, set: setExamCost, min: 50, max: 500 },
              { label: "Guided pass rate (%)", value: guidedRate, set: setGuidedRate, min: 50, max: 100 },
              { label: "Unguided pass rate (%)", value: unguidedRate, set: setUnguidedRate, min: 20, max: 90 },
              { label: "Avg study weeks", value: studyWeeks, set: setStudyWeeks, min: 1, max: 20 },
            ].map(({ label, value, set, min, max }) => (
              <div key={label}>
                <label className="text-[#8b949e] text-sm block mb-1">{label}</label>
                <input
                  type="number"
                  min={min}
                  max={max}
                  value={value}
                  onChange={(e) => set(Number(e.target.value))}
                  className={INPUT_CLASS}
                />
              </div>
            ))}
          </div>

          <div className="mt-6 border-t border-[#21262d] pt-5 space-y-2 text-sm">
            {[
              { label: "Exam cost", value: `$${examCost}/attempt` },
              { label: "Unguided pass rate", value: `${unguidedRate}%`, color: "text-[#f85149]" },
              { label: "CertifyIQ pass rate", value: `${guidedRate}%`, color: "text-[#3fb950]" },
            ].map((row) => (
              <div key={row.label} className="flex justify-between">
                <span className="text-[#6e7681]">{row.label}</span>
                <span className={row.color || "text-[#f0f6fc]"}>{row.value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Live output */}
        <div>
          <p className="text-[#6e7681] text-xs uppercase tracking-widest mb-5">Live results</p>

          {/* Big number */}
          <div className="bg-[#0d1117] border border-[#238636]/30 rounded-lg p-5 mb-4">
            <p className="text-[#3fb950] text-5xl font-mono font-bold">${totalROI.toFixed(0)}</p>
            <p className="text-[#6e7681] text-sm mt-1">total ROI for {teamSize}-person team</p>
          </div>

          {/* Comparison table */}
          <div className="bg-[#0d1117] border border-[#21262d] rounded-lg overflow-hidden mb-4">
            <table className="w-full text-xs font-mono">
              <thead>
                <tr className="border-b border-[#21262d]">
                  <th className="text-left px-4 py-2.5 text-[#6e7681]"></th>
                  <th className="text-right px-4 py-2.5 text-[#6e7681]">Unguided</th>
                  <th className="text-right px-4 py-2.5 text-[#6e7681]">Guided</th>
                  <th className="text-right px-4 py-2.5 text-[#3fb950]">Saved</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-[#21262d]">
                  <td className="px-4 py-2.5 text-[#8b949e]">Avg attempts</td>
                  <td className="px-4 py-2.5 text-right text-[#f85149]">{unguidedAttempts.toFixed(2)}×</td>
                  <td className="px-4 py-2.5 text-right text-[#3fb950]">{guidedAttempts.toFixed(2)}×</td>
                  <td className="px-4 py-2.5 text-right text-[#3fb950]">{(unguidedAttempts - guidedAttempts).toFixed(2)}×</td>
                </tr>
                <tr className="border-b border-[#21262d]">
                  <td className="px-4 py-2.5 text-[#8b949e]">Cost/employee</td>
                  <td className="px-4 py-2.5 text-right text-[#f85149]">${unguidedCost.toFixed(0)}</td>
                  <td className="px-4 py-2.5 text-right text-[#3fb950]">${guidedCost.toFixed(0)}</td>
                  <td className="px-4 py-2.5 text-right text-[#3fb950]">${costSavingsPerEmp.toFixed(0)}</td>
                </tr>
                <tr>
                  <td className="px-4 py-2.5 text-[#8b949e]">Team total</td>
                  <td className="px-4 py-2.5 text-right text-[#f85149]">${(unguidedCost * teamSize).toFixed(0)}</td>
                  <td className="px-4 py-2.5 text-right text-[#3fb950]">${(guidedCost * teamSize).toFixed(0)}</td>
                  <td className="px-4 py-2.5 text-right font-bold text-[#3fb950]">${(costSavingsPerEmp * teamSize).toFixed(0)}</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Projection */}
          <div className="bg-[#0d1117] border border-[#21262d] rounded-lg p-4 mb-4">
            <p className="text-[#6e7681] text-xs uppercase tracking-widest mb-3">Projection</p>
            <div className="grid grid-cols-3 gap-3">
              {[{ label: "1 year", value: yr1 }, { label: "3 years", value: yr3 }, { label: "5 years", value: yr5 }].map((p) => (
                <div key={p.label}>
                  <p className="text-[#6e7681] text-xs mb-1">{p.label}</p>
                  <p className="text-[#3fb950] font-mono font-bold text-sm">${p.value.toFixed(0)}</p>
                </div>
              ))}
            </div>
          </div>

          <p className="text-[#6e7681] text-xs">Source: Certification ROI & Cost Analysis — CertifyIQ Knowledge Base</p>

          <button className="mt-3 text-[#8b949e] text-xs hover:text-[#f0f6fc] transition-colors">
            Download as PDF →
          </button>
        </div>
      </div>

      <div className="mt-8 pt-6 border-t border-[#21262d]">
        <a href="/" className="text-xs text-[#6e7681] hover:text-[#f0f6fc] transition-colors">
          ← Back to home
        </a>
      </div>
    </div>
  );
}