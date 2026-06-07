"use client";

import { usePathname } from "next/navigation";

const NAV_ITEMS = [
  { label: "Overview", href: "/" },
  { label: "Analyze", href: "/certify/EMP-001" },
  { label: "Team", href: "/dashboard" },
  { label: "ROI", href: "/roi" },
  { label: "Business", href: "/business" },
];

function isActive(pathname: string, href: string): boolean {
  if (href === "/") return pathname === "/";
  if (href.startsWith("/certify")) return pathname.startsWith("/certify");
  return pathname.startsWith(href);
}

export default function NavBar() {
  const pathname = usePathname();

  return (
    <nav
      className="sticky top-0 z-40 h-12 border-b border-[#21262d] w-full"
      style={{ background: "rgba(13,17,23,0.95)", backdropFilter: "blur(8px)" }}
    >
      <div className="max-w-7xl mx-auto px-6 h-full flex items-center justify-between">
        {/* Logo */}
        <a href="/" className="flex items-center shrink-0">
          <span className="font-semibold text-[#f0f6fc] text-base tracking-tight">certify</span>
          <span className="font-bold text-[#1f6feb] text-base tracking-tight">IQ</span>
        </a>

        {/* Pill nav */}
        <div className="inline-flex items-center gap-0.5 bg-[#161b22] rounded-full px-1 py-1">
          {NAV_ITEMS.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className={`px-3 py-1.5 rounded-full text-sm transition-colors ${
                isActive(pathname, item.href)
                  ? "bg-[#21262d] text-[#f0f6fc]"
                  : "text-[#8b949e] hover:text-[#f0f6fc]"
              }`}
            >
              {item.label}
            </a>
          ))}
        </div>

        {/* Right side */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-[#3fb950]" />
            <span className="text-[#6e7681] text-xs">Foundry IQ</span>
          </div>
          <div className="w-px h-4 bg-[#21262d]" />
          <span className="text-[#8b949e] text-xs">Demo User</span>
          <span className="text-[#21262d]">|</span>
          <button className="text-[#6e7681] text-xs hover:text-[#f0f6fc] transition-colors cursor-pointer">
            Sign out
          </button>
        </div>
      </div>
    </nav>
  );
}