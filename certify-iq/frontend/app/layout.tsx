import type { Metadata } from "next";
import "./globals.css";
import NavBar from "./components/NavBar";
import AIAssistant from "./components/AIAssistant";

export const metadata: Metadata = {
  title: "CertifyIQ — Workforce AI Readiness Intelligence",
  description:
    "CertifyIQ predicts certification failure 6 weeks before it happens. 10 reasoning agents, Azure Foundry IQ grounding, 25-rule guardrail pipeline.",
};

function Footer() {
  return (
    <footer className="bg-[#0d1117] border-t border-[#21262d] py-4 w-full">
      <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
        <div>
          <span className="text-[#6e7681] text-xs">CertifyIQ</span>
          <span className="text-[#6e7681] text-xs ml-2">© 2026</span>
        </div>
        <span className="text-[#6e7681] text-xs">Built on Azure AI Foundry IQ</span>
        <div className="flex items-center gap-4">
          <a
            href="https://github.com/saksham869/ELCMS"
            className="text-[#6e7681] text-xs hover:text-[#f0f6fc] transition-colors"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub →
          </a>
          <a href="/business" className="text-[#6e7681] text-xs hover:text-[#f0f6fc] transition-colors">
            Business
          </a>
          <a href="/audit" className="text-[#6e7681] text-xs hover:text-[#f0f6fc] transition-colors">
            Audit
          </a>
        </div>
      </div>
    </footer>
  );
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen text-[#f0f6fc] antialiased flex flex-col">
        <NavBar />
        <main className="flex-1">{children}</main>
        <Footer />
        <AIAssistant />
      </body>
    </html>
  );
}