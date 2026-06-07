"use client";

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

const MARKET_DATA = [
  { year: "2025", value: 20.4 },
  { year: "2026", value: 23.5 },
  { year: "2027", value: 27.0 },
  { year: "2028", value: 31.0 },
  { year: "2029", value: 35.7 },
  { year: "2030", value: 41.0 },
  { year: "2031", value: 47.2 },
  { year: "2032", value: 54.1 },
];

const PRICING = [
  {
    name: "Starter",
    price: "$12",
    per: "/emp/mo",
    size: "≤50 employees",
    cta: "Start free trial",
    popular: false,
  },
  {
    name: "Growth",
    price: "$9",
    per: "/emp/mo",
    size: "50–500 employees",
    cta: "Most popular",
    popular: true,
  },
  {
    name: "Enterprise",
    price: "Custom",
    per: "",
    size: "500+ employees",
    cta: "Contact sales",
    popular: false,
  },
];

const FEATURES = [
  { name: "10 AI agents", starter: true, growth: true, enterprise: true },
  { name: "Foundry IQ grounding", starter: true, growth: true, enterprise: true },
  { name: "Manager dashboard", starter: true, growth: true, enterprise: true },
  { name: "Peer benchmarking", starter: false, growth: true, enterprise: true },
  { name: "ROI calculator", starter: false, growth: true, enterprise: true },
  { name: "Intervention emails", starter: false, growth: true, enterprise: true },
  { name: "Custom cert tracks", starter: false, growth: false, enterprise: true },
  { name: "SLA guarantee", starter: false, growth: false, enterprise: true },
  { name: "Azure Marketplace listing", starter: false, growth: false, enterprise: true },
];

const GTM = [
  {
    channel: "Azure Marketplace",
    icon: "◈",
    stat: "95,000+",
    statLabel: "enterprise customers",
    text: "Zero sales team required for first 100 customers. Listed as a verified Azure-native solution. Procurement through existing Azure subscription.",
  },
  {
    channel: "Microsoft Partner Network",
    icon: "⬡",
    stat: "400,000+",
    statLabel: "Microsoft partners",
    text: "Partners need certified staff for client contracts. CertifyIQ directly reduces the cost of partner compliance and contract qualification.",
  },
  {
    channel: "Direct L&D",
    icon: "◎",
    stat: "50-500",
    statLabel: "employee sweet spot",
    text: "LinkedIn Sales Navigator targeting L&D directors at Azure-heavy companies. $165 cost-per-exam is the hook that gets CFO approval.",
  },
];

const REVENUE = [
  { year: "Y1", customers: 50, avgTeam: 100, arr: "$540K" },
  { year: "Y2", customers: 200, avgTeam: 150, arr: "$3.24M" },
  { year: "Y3", customers: 1000, avgTeam: 180, arr: "$19.44M" },
];

const TECH_PROOF = [
  "Azure AI Foundry IQ — GA at Build 2026 (June 2, 2026)",
  "GitHub Models GPT-4o — Tier 1 LLM via verified Microsoft endpoint",
  "25-rule responsible AI guardrail pipeline — input, output, bias",
  "4-tier LLM fallback — Azure → OpenAI → Anthropic → Mock",
  "44 automated tests — agents, guardrails, orchestrator, SSE",
  "Sub-10ms mock engine — demo reliability guaranteed",
];

export default function BusinessPage() {
  return (
    <div className="max-w-4xl mx-auto px-6 py-12">

      {/* ─── SECTION 1: The Problem ─── */}
      <section className="mb-20">
        <p className="text-[#6e7681] text-xs uppercase tracking-widest mb-6">The Problem</p>
        <h2 className="text-[#f0f6fc] text-3xl font-bold mb-8">The Azure ROI Gap</h2>

        <div className="border-l-2 border-[#1f6feb] pl-6 mb-10">
          <p className="text-[#f0f6fc] text-xl leading-relaxed">
            &ldquo;Organizations invest $X in Azure.
            <br />
            Then lose the return because their
            <br />
            teams aren&apos;t certified to use it.&rdquo;
          </p>
        </div>

        <div className="flex items-center gap-8">
          {[
            { value: "$5.5T", label: "skills gap cost (IDC, 2026)" },
            { value: "90%", label: "enterprises face shortages" },
            { value: "$165", label: "per failed exam attempt" },
          ].map((stat) => (
            <div key={stat.value}>
              <p className="text-[#f0f6fc] text-4xl font-mono font-bold">{stat.value}</p>
              <p className="text-[#6e7681] text-xs mt-1">{stat.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ─── SECTION 2: Market Size ─── */}
      <section className="mb-20 border-t border-[#21262d] pt-12">
        <p className="text-[#6e7681] text-xs uppercase tracking-widest mb-6">Market Size</p>
        <h2 className="text-[#f0f6fc] text-3xl font-bold mb-2">$20.4B in 2025. $54.1B by 2032.</h2>
        <p className="text-[#8b949e] text-sm mb-8">14.95% CAGR. Certification management software.</p>

        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={MARKET_DATA} margin={{ left: -10 }}>
            <XAxis dataKey="year" tick={{ fill: "#6e7681", fontSize: 11 }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fill: "#6e7681", fontSize: 11 }} axisLine={false} tickLine={false} unit="B" />
            <Tooltip
              contentStyle={{ background: "#0d1117", border: "1px solid #21262d", borderRadius: "6px", fontSize: "12px" }}
              labelStyle={{ color: "#f0f6fc" }}
              formatter={(v: number) => [`$${v}B`, "Market Size"]}
            />
            <Bar dataKey="value" radius={[3, 3, 0, 0]} maxBarSize={36}>
              {MARKET_DATA.map((_, i) => (
                <Cell key={i} fill={i < 2 ? "#1f6feb" : "#6e40c9"} fillOpacity={0.6 + (i / MARKET_DATA.length) * 0.4} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </section>

      {/* ─── SECTION 3: Why Now ─── */}
      <section className="mb-20 border-t border-[#21262d] pt-12">
        <p className="text-[#6e7681] text-xs uppercase tracking-widest mb-6">Why Now</p>
        <h2 className="text-[#f0f6fc] text-3xl font-bold mb-8">Three forces converging in 2026</h2>

        <div className="grid grid-cols-3 gap-4">
          {[
            {
              title: "Microsoft IQ went GA at Build 2026",
              text: "The intelligence layer CertifyIQ builds on became generally available on June 2, 2026. CertifyIQ is first-mover on the GA stack.",
            },
            {
              title: "250+ Microsoft certs. Growing 40% annually.",
              text: "The exam surface area is expanding faster than any workforce can track manually. CertifyIQ scales with the certification catalog.",
            },
            {
              title: "AI readiness gap = competitive disadvantage",
              text: "Microsoft research: AI leaders report 47–64% stronger performance. Only 17.7% of organisations qualify. The gap is measurable.",
            },
          ].map((card) => (
            <div key={card.title} className="bg-[#0d1117] border border-[#21262d] rounded-lg p-5">
              <h3 className="text-[#f0f6fc] text-sm font-semibold mb-3">{card.title}</h3>
              <p className="text-[#8b949e] text-xs leading-relaxed">{card.text}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ─── SECTION 4: Solution ─── */}
      <section className="mb-20 border-t border-[#21262d] pt-12">
        <p className="text-[#6e7681] text-xs uppercase tracking-widest mb-6">Solution</p>
        <h2 className="text-[#f0f6fc] text-3xl font-bold mb-3">
          CertifyIQ is the intelligence layer
          <br />
          that sits above your LMS.
        </h2>
        <p className="text-[#8b949e] text-sm mb-8">
          Existing tools deliver content. CertifyIQ delivers intelligence.
        </p>

        {/* Architecture diagram */}
        <div className="max-w-md border border-[#21262d] rounded-lg overflow-hidden font-mono text-xs mb-8">
          <div className="bg-[#6e40c9]/10 border-b border-[#21262d] p-4 text-center">
            <p className="text-[#a371f7] font-semibold">CertifyIQ</p>
            <p className="text-[#6e7681]">Readiness · Prevention · ROI</p>
          </div>
          <div className="grid grid-cols-3 divide-x divide-[#21262d]">
            {["Microsoft Learn", "Pluralsight", "Viva Learning"].map((n) => (
              <div key={n} className="p-3 text-center text-[#6e7681]">{n}</div>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          {[
            { persona: "L&D Manager", quote: "I need to prove training ROI to my CFO" },
            { persona: "Engineering Manager", quote: "I need my team certified for Q3" },
            { persona: "Microsoft Partner", quote: "I lose contracts when certs lapse" },
          ].map((p) => (
            <div key={p.persona} className="border border-[#21262d] rounded-lg p-4">
              <p className="text-[#1f6feb] text-xs mb-2">{p.persona}</p>
              <p className="text-[#8b949e] text-xs italic">&ldquo;{p.quote}&rdquo;</p>
            </div>
          ))}
        </div>
      </section>

      {/* ─── SECTION 5: Pricing ─── */}
      <section className="mb-20 border-t border-[#21262d] pt-12">
        <p className="text-[#6e7681] text-xs uppercase tracking-widest mb-6">Pricing</p>
        <h2 className="text-[#f0f6fc] text-3xl font-bold mb-8">Simple. Predictable. Per seat.</h2>

        <div className="grid grid-cols-3 gap-4 mb-8">
          {PRICING.map((plan) => (
            <div
              key={plan.name}
              className={`border rounded-lg p-5 ${
                plan.popular ? "border-[#1f6feb] bg-[#1f6feb]/5" : "border-[#21262d] bg-[#0d1117]"
              }`}
            >
              {plan.popular && (
                <span className="text-[10px] text-[#1f6feb] font-mono uppercase tracking-widest mb-3 block">
                  Most popular
                </span>
              )}
              <h3 className="text-[#f0f6fc] font-semibold mb-1">{plan.name}</h3>
              <div className="flex items-baseline gap-0.5 mb-1">
                <span className="text-[#f0f6fc] text-3xl font-mono font-bold">{plan.price}</span>
                <span className="text-[#6e7681] text-sm">{plan.per}</span>
              </div>
              <p className="text-[#6e7681] text-xs mb-4">{plan.size}</p>
              <button
                className={`w-full py-2 text-xs rounded font-medium transition-colors ${
                  plan.popular
                    ? "bg-[#1f6feb] hover:bg-[#388bfd] text-white"
                    : "border border-[#30363d] text-[#8b949e] hover:text-[#f0f6fc]"
                }`}
              >
                {plan.cta}
              </button>
            </div>
          ))}
        </div>

        {/* Feature table */}
        <div className="border border-[#21262d] rounded-lg overflow-hidden">
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-[#21262d]">
                <th className="text-left px-4 py-2.5 text-[#6e7681]">Feature</th>
                {PRICING.map((p) => (
                  <th key={p.name} className={`px-4 py-2.5 text-center ${p.popular ? "text-[#1f6feb]" : "text-[#6e7681]"}`}>
                    {p.name}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {FEATURES.map((feat, i) => (
                <tr key={feat.name} className={`border-b border-[#21262d] ${i % 2 === 0 ? "" : "bg-[#0d1117]"}`}>
                  <td className="px-4 py-2.5 text-[#8b949e]">{feat.name}</td>
                  <td className="px-4 py-2.5 text-center">{feat.starter ? <span className="text-[#3fb950]">✓</span> : <span className="text-[#30363d]">✗</span>}</td>
                  <td className="px-4 py-2.5 text-center">{feat.growth ? <span className="text-[#3fb950]">✓</span> : <span className="text-[#30363d]">✗</span>}</td>
                  <td className="px-4 py-2.5 text-center">{feat.enterprise ? <span className="text-[#3fb950]">✓</span> : <span className="text-[#30363d]">✗</span>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* ─── SECTION 6: Go-to-Market ─── */}
      <section className="mb-20 border-t border-[#21262d] pt-12">
        <p className="text-[#6e7681] text-xs uppercase tracking-widest mb-6">Go-to-Market</p>
        <h2 className="text-[#f0f6fc] text-3xl font-bold mb-8">Three channels. Zero guessing.</h2>

        <div className="space-y-4">
          {GTM.map((channel) => (
            <div key={channel.channel} className="bg-[#0d1117] border border-[#21262d] rounded-lg p-5 flex gap-6">
              <div>
                <span className="text-[#6e40c9] text-2xl">{channel.icon}</span>
              </div>
              <div className="flex-1">
                <h3 className="text-[#f0f6fc] text-sm font-semibold mb-1">{channel.channel}</h3>
                <p className="text-[#8b949e] text-xs leading-relaxed">{channel.text}</p>
              </div>
              <div className="text-right shrink-0">
                <p className="text-[#f0f6fc] text-xl font-mono font-bold">{channel.stat}</p>
                <p className="text-[#6e7681] text-xs">{channel.statLabel}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ─── SECTION 7: Revenue Model ─── */}
      <section className="mb-20 border-t border-[#21262d] pt-12">
        <p className="text-[#6e7681] text-xs uppercase tracking-widest mb-6">Revenue Model</p>
        <h2 className="text-[#f0f6fc] text-3xl font-bold mb-3">1% of the addressable market.</h2>
        <p className="text-[#8b949e] text-sm mb-8">Conservative projections. No hockey stick assumptions.</p>

        <div className="border border-[#21262d] rounded-lg overflow-hidden mb-4">
          <table className="w-full text-sm font-mono">
            <thead>
              <tr className="border-b border-[#21262d]">
                {["Year", "Customers", "Avg Team", "ARR"].map((h) => (
                  <th key={h} className="text-left px-5 py-3 text-[#6e7681] text-xs uppercase tracking-widest">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {REVENUE.map((row, i) => (
                <tr key={row.year} className={`border-b border-[#21262d] last:border-0 ${i === 2 ? "bg-[#0d1117]" : ""}`}>
                  <td className="px-5 py-3 text-[#8b949e]">{row.year}</td>
                  <td className="px-5 py-3 text-[#f0f6fc]">{row.customers}</td>
                  <td className="px-5 py-3 text-[#f0f6fc]">{row.avgTeam}</td>
                  <td className={`px-5 py-3 font-bold ${i === 2 ? "text-[#3fb950]" : "text-[#f0f6fc]"}`}>{row.arr}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="text-[#6e7681] text-xs font-mono">1% penetration of $20.4B addressable market · Growth tier avg pricing</p>
      </section>

      {/* ─── SECTION 8: Technical Moat ─── */}
      <section className="mb-12 border-t border-[#21262d] pt-12">
        <p className="text-[#6e7681] text-xs uppercase tracking-widest mb-6">Technical Moat</p>
        <h2 className="text-[#f0f6fc] text-3xl font-bold mb-3">Built on Microsoft&apos;s own intelligence layer.</h2>
        <p className="text-[#8b949e] text-sm mb-8">
          Every competitor would have to rebuild what CertifyIQ already has running in production.
        </p>

        <div className="space-y-2">
          {TECH_PROOF.map((point) => (
            <div key={point} className="flex items-start gap-3 py-2.5 border-b border-[#21262d]">
              <span className="text-[#3fb950] text-xs mt-0.5 shrink-0">✓</span>
              <p className="text-[#8b949e] text-sm">{point}</p>
            </div>
          ))}
        </div>

        <div className="mt-10 p-5 bg-[#0d1117] border border-[#21262d] rounded-lg">
          <p className="text-[#f0f6fc] font-semibold mb-1">This could ship tomorrow.</p>
          <p className="text-[#8b949e] text-sm">
            CertifyIQ is not a demo. It runs real Azure AI Search queries, real GPT-4o completions via GitHub Models,
            and a 25-rule guardrail pipeline validated by 44 automated tests. The gap between prototype and production
            is narrower than any other submission in this track.
          </p>
        </div>
      </section>

      <div className="border-t border-[#21262d] pt-6 flex gap-6">
        <a href="/" className="text-xs text-[#6e7681] hover:text-[#f0f6fc] transition-colors">← Home</a>
        <a href="/dashboard" className="text-xs text-[#6e7681] hover:text-[#f0f6fc] transition-colors">Team Dashboard →</a>
        <a href="/roi" className="text-xs text-[#6e7681] hover:text-[#f0f6fc] transition-colors">ROI Calculator →</a>
      </div>
    </div>
  );
}