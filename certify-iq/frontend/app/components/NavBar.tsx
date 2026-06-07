"use client";

import { usePathname } from "next/navigation";

const NAV_ITEMS = [
  { label: "Overview", href: "/" },
  { label: "Analyze", href: "/#start" },
  { label: "Team", href: "/dashboard" },
  { label: "ROI", href: "/roi" },
  { label: "Business", href: "/business" },
];

function isActive(pathname: string, href: string): boolean {
  if (href === "/" || href === "/#start") return pathname === "/";
  return pathname.startsWith(href);
}

export default function NavBar() {
  const pathname = usePathname();

  return (
    <nav
      className="sticky top-0 z-50 h-12 border-b border-[#21262d] flex items-center px-6"
      style={{ background: "rgba(3,7,18,0.95)", backdropFilter: "blur(8px)" }}
    >
      {/* Logo */}
      <a href="/" className="flex items-center gap-0 mr-8 shrink-0">
        <span className="font-medium text-[#f0f6fc] text-sm tracking-tight">certify</span>
        <span className="font-bold text-[#1f6feb] text-sm tracking-tight">IQ</span>
      </a>

      {/* Pill nav */}
      <div className="flex items-center gap-0.5 bg-[#0d1117] rounded-full px-1 py-1">
        {NAV_ITEMS.map((item) => (
          <a
            key={item.href}
            href={item.href}
            className={`px-3 py-1 rounded-full text-xs transition-colors ${
              isActive(pathname, item.href)
                ? "bg-[#161b22] text-[#f0f6fc]"
                : "text-[#8b949e] hover:text-[#f0f6fc]"
            }`}
          >
            {item.label}
          </a>
        ))}
      </div>

      {/* Right side */}
      <div className="ml-auto flex items-center gap-3">
        <div className="flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-[#3fb950]" />
          <span className="text-[#6e7681] text-xs">Foundry IQ connected</span>
        </div>
        <span className="text-[#30363d]">|</span>
        <a
          href="/business"
          className="text-[#8b949e] text-xs hover:text-[#f0f6fc] transition-colors"
        >
          Business case →
        </a>
      </div>
    </nav>
  );
}