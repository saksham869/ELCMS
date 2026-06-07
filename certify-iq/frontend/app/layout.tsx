import type { Metadata } from "next";
import "./globals.css";
import NavBar from "./components/NavBar";

export const metadata: Metadata = {
  title: "CertifyIQ — Workforce AI Readiness Intelligence",
  description:
    "CertifyIQ predicts certification failure 6 weeks before it happens. 10 reasoning agents, Azure Foundry IQ grounding, 25-rule guardrail pipeline.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen text-[#f0f6fc] antialiased">
        <NavBar />
        <main>{children}</main>
      </body>
    </html>
  );
}