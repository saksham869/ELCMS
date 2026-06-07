"use client";

import { useState } from "react";

const EXAM_COST = 165;
const UNGUIDED_PASS_RATE = 0.58;
const GUIDED_PASS_RATE = 0.89;
const PRODUCTIVITY_LOSS_PER_WEEK = 200;

export default function ROIPage() {
  const [employees, setEmployees] = useState(10);
  const [weeks, setWeeks] = useState(6);
  const [failedRetakes, setFailedRetakes] = useState(1);

  const unguidedAttempts = 1 / UNGUIDED_PASS_RATE;
  const guidedAttempts = 1 / GUIDED_PASS_RATE;

  const unguidedCostPerEmp = unguidedAttempts * EXAM_COST;
  const guidedCostPerEmp = guidedAttempts * EXAM_COST;

  const costSavingsPerEmp = unguidedCostPerEmp - guidedCostPerEmp;
  const productivitySavingsPerEmp = weeks * PRODUCTIVITY_LOSS_PER_WEEK * 0.3;
  const totalROIPerEmp = costSavingsPerEmp + productivitySavingsPerEmp;

  const totalROI = totalROIPerEmp * employees;

  return (
    <div className="max-w-4xl mx-auto px-6 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">ROI Calculator</h1>
        <p className="text-gray-400 mt-1">
          Calculate the financial impact of CertifyIQ-guided vs unguided exam preparation
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {/* Controls */}
        <div className="bg-[#0d1429] border border-white/10 rounded-2xl p-6 space-y-6">
          <h2 className="font-semibold text-white">Parameters</h2>

          <div>
            <label className="text-sm text-gray-400 block mb-2">
              Number of Employees: <span className="text-white font-bold">{employees}</span>
            </label>
            <input
              type="range"
              min={1}
              max={100}
              value={employees}
              onChange={(e) => setEmployees(Number(e.target.value))}
              className="w-full accent-blue-500"
            />
          </div>

          <div>
            <label className="text-sm text-gray-400 block mb-2">
              Study Plan Weeks: <span className="text-white font-bold">{weeks}</span>
            </label>
            <input
              type="range"
              min={2}
              max={12}
              value={weeks}
              onChange={(e) => setWeeks(Number(e.target.value))}
              className="w-full accent-purple-500"
            />
          </div>

          <div className="bg-white/5 rounded-xl p-4 text-sm space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-400">Exam Cost</span>
              <span className="text-white">${EXAM_COST}/attempt</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Unguided Pass Rate</span>
              <span className="text-red-300">{(UNGUIDED_PASS_RATE * 100).toFixed(0)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">CertifyIQ Pass Rate</span>
              <span className="text-green-300">{(GUIDED_PASS_RATE * 100).toFixed(0)}%</span>
            </div>
          </div>
        </div>

        {/* Results */}
        <div className="space-y-4">
          <div className="bg-green-500/10 border border-green-500/30 rounded-2xl p-6">
            <p className="text-sm text-gray-400 mb-1">Total ROI</p>
            <p className="text-4xl font-bold text-green-400">${totalROI.toFixed(0)}</p>
            <p className="text-sm text-gray-500 mt-1">across {employees} employees</p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-[#0d1429] border border-white/10 rounded-xl p-4">
              <p className="text-xs text-gray-500 mb-1">Cost Savings/Emp</p>
              <p className="text-xl font-bold text-blue-400">${costSavingsPerEmp.toFixed(0)}</p>
              <p className="text-xs text-gray-600">from fewer retakes</p>
            </div>
            <div className="bg-[#0d1429] border border-white/10 rounded-xl p-4">
              <p className="text-xs text-gray-500 mb-1">Productivity/Emp</p>
              <p className="text-xl font-bold text-purple-400">${productivitySavingsPerEmp.toFixed(0)}</p>
              <p className="text-xs text-gray-600">recovered output</p>
            </div>
          </div>

          <div className="bg-[#0d1429] border border-white/10 rounded-xl p-4 space-y-3">
            <h3 className="text-sm font-semibold text-white">Comparison</h3>
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">Unguided avg attempts</span>
              <span className="text-red-300">{unguidedAttempts.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">CertifyIQ avg attempts</span>
              <span className="text-green-300">{guidedAttempts.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm border-t border-white/5 pt-2">
              <span className="text-gray-400">ROI per employee</span>
              <span className="text-white font-bold">${totalROIPerEmp.toFixed(0)}</span>
            </div>
          </div>
        </div>
      </div>

      <p className="text-xs text-gray-600 text-center">
        Source: Certification ROI & Cost Analysis — CertifyIQ Knowledge Base
      </p>

      <div className="mt-6 text-center">
        <a href="/" className="text-sm text-gray-500 hover:text-white transition-colors">
          ← Back to home
        </a>
      </div>
    </div>
  );
}