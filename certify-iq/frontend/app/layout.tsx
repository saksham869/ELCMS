import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CertifyIQ — Enterprise Workforce Intelligence",
  description:
    "AI-powered certification readiness platform with 10 reasoning agents, Azure AI Foundry IQ grounding, and 25-rule responsible AI guardrails.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#0a0f1e] text-white antialiased">
        <nav className="border-b border-white/10 bg-[#0d1429]/80 backdrop-blur-sm sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
            <a href="/" className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-sm font-bold">
                C
              </div>
              <span className="font-bold text-lg tracking-tight">CertifyIQ</span>
              <span className="text-xs bg-blue-500/20 text-blue-300 px-2 py-0.5 rounded-full border border-blue-500/30">
                v3.0
              </span>
            </a>
            <div className="flex items-center gap-6 text-sm text-gray-400">
              <a href="/" className="hover:text-white transition-colors">
                Home
              </a>
              <a href="/dashboard" className="hover:text-white transition-colors">
                Dashboard
              </a>
              <a href="/roi" className="hover:text-white transition-colors">
                ROI
              </a>
              <a href="/audit" className="hover:text-white transition-colors">
                Audit
              </a>
            </div>
          </div>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  );
}
