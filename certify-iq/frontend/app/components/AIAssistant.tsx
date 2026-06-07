"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import { AnimatePresence, motion } from "framer-motion";

const EMPLOYEE_MAP: Record<string, { id: string; name: string }> = {
  "morgan lee": { id: "EMP-003", name: "Morgan Lee" },
  "alex chen": { id: "EMP-001", name: "Alex Chen" },
  "jordan smith": { id: "EMP-002", name: "Jordan Smith" },
  "riley park": { id: "EMP-004", name: "Riley Park" },
};

const SUGGESTIONS = [
  "Who is most at risk?",
  "What's our budget exposure?",
  "Which exam is soonest?",
];

type Role = "user" | "assistant" | "loading";

interface Message {
  id: string;
  role: Role;
  text: string;
  citations?: string[];
  action?: { label: string; href: string };
}

function LoadingDots() {
  return (
    <div className="flex items-center gap-1.5 py-1">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="w-1.5 h-1.5 rounded-full bg-[#6e7681]"
          style={{ animation: `pulse 1.2s ease-in-out ${i * 0.2}s infinite` }}
        />
      ))}
      <span className="text-[#6e7681] text-xs ml-1">Querying Foundry IQ...</span>
    </div>
  );
}

function CitationChip({ label }: { label: string }) {
  return (
    <span className="inline-flex items-center gap-1 bg-[#0d1117] border border-[#30363d] text-[#6e7681] text-xs rounded px-2 py-0.5">
      📄 {label}
    </span>
  );
}

function ActionChip({ label, onClick }: { label: string; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="inline-flex items-center gap-1 bg-[#da3633]/10 border border-[#da3633]/30 text-[#f85149] text-xs rounded px-2 py-0.5 hover:bg-[#da3633]/20 transition-colors cursor-pointer"
    >
      → {label}
    </button>
  );
}

function MessageBubble({ msg, onAction }: { msg: Message; onAction: (href: string) => void }) {
  if (msg.role === "loading") {
    return (
      <div className="mr-auto bg-[#161b22] border border-[#21262d] rounded-xl rounded-bl-sm px-3 py-2 max-w-[85%]">
        <LoadingDots />
      </div>
    );
  }

  if (msg.role === "user") {
    return (
      <div className="ml-auto bg-[#1f6feb] text-white text-sm rounded-xl rounded-br-sm px-3 py-2 max-w-[80%]">
        {msg.text}
      </div>
    );
  }

  return (
    <div className="mr-auto bg-[#161b22] border border-[#21262d] text-[#f0f6fc] text-sm rounded-xl rounded-bl-sm px-3 py-2 max-w-[85%] space-y-2">
      <p className="leading-relaxed">{msg.text}</p>
      {msg.citations && msg.citations.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {msg.citations.map((c) => (
            <CitationChip key={c} label={c} />
          ))}
        </div>
      )}
      {msg.action && (
        <ActionChip label={msg.action.label} onClick={() => onAction(msg.action!.href)} />
      )}
    </div>
  );
}

export default function AIAssistant() {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 300);
    }
  }, [open]);

  async function submit(question: string) {
    const q = question.trim();
    if (!q || loading) return;

    const userMsg: Message = { id: crypto.randomUUID(), role: "user", text: q };
    const loadingMsg: Message = { id: "loading", role: "loading", text: "" };

    setMessages((prev) => [...prev.slice(-9), userMsg, loadingMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });

      if (!res.ok) throw new Error("API error");

      const data = await res.json();
      const answer: string = data.answer || "No answer returned.";
      const citations: string[] = (data.citations || []).slice(0, 3);
      const employees: string[] = data.relevant_employees || [];

      let action: Message["action"] | undefined;
      const lowerAnswer = answer.toLowerCase();
      for (const [key, emp] of Object.entries(EMPLOYEE_MAP)) {
        if (employees.includes(emp.id) || lowerAnswer.includes(key)) {
          action = { label: `Analyze ${emp.name}`, href: `/certify/${emp.id}` };
          break;
        }
      }

      const assistantMsg: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        text: answer,
        citations,
        action,
      };

      setMessages((prev) => [...prev.filter((m) => m.id !== "loading"), assistantMsg]);
    } catch {
      const errMsg: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        text: "I couldn't reach the knowledge base. Please try again in a moment.",
        citations: [],
      };
      setMessages((prev) => [...prev.filter((m) => m.id !== "loading"), errMsg]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit(input);
    }
  }

  function handleAction(href: string) {
    setOpen(false);
    router.push(href);
  }

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
            className="flex flex-col bg-[#0d1117] border border-[#21262d] rounded-2xl shadow-2xl shadow-black/50 overflow-hidden"
            style={{ width: 380, height: 520 }}
          >
            {/* Header */}
            <div className="flex items-center justify-between bg-[#161b22] border-b border-[#21262d] px-4 py-3 shrink-0">
              <div>
                <div className="flex items-center gap-1.5">
                  <span className="text-[#1f6feb] font-medium">✦</span>
                  <span className="text-[#f0f6fc] text-sm font-medium">CertifyIQ Assistant</span>
                </div>
                <p className="text-[#6e7681] text-xs mt-0.5">Powered by Azure Foundry IQ</p>
              </div>
              <div className="flex items-center gap-1">
                <button
                  onClick={() => setOpen(false)}
                  className="w-6 h-6 rounded flex items-center justify-center text-[#6e7681] hover:text-[#f0f6fc] hover:bg-[#21262d] transition-colors text-xs"
                  title="Minimize"
                >
                  —
                </button>
                <button
                  onClick={() => setOpen(false)}
                  className="w-6 h-6 rounded flex items-center justify-center text-[#6e7681] hover:text-[#f0f6fc] hover:bg-[#21262d] transition-colors text-sm"
                  title="Close"
                >
                  ×
                </button>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3 min-h-0">
              {/* Welcome */}
              <div className="bg-[#161b22] border border-[#21262d] rounded-xl p-3 text-[#8b949e] text-sm">
                👋 Ask me anything about your team's certification readiness. I'm grounded in your Foundry IQ knowledge base.
              </div>

              {messages.map((msg) => (
                <MessageBubble key={msg.id} msg={msg} onAction={handleAction} />
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Suggestions */}
            <div className="bg-[#0d1117] border-t border-[#21262d] px-3 py-2 flex flex-wrap gap-1.5 shrink-0">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => submit(s)}
                  disabled={loading}
                  className="bg-[#161b22] border border-[#30363d] text-[#8b949e] text-xs rounded-full px-3 py-1.5 hover:border-[#1f6feb] hover:text-[#58a6ff] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  {s}
                </button>
              ))}
            </div>

            {/* Input */}
            <div className="bg-[#0d1117] border-t border-[#21262d] px-3 py-3 flex gap-2 items-center shrink-0">
              <input
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={loading}
                placeholder="Ask anything..."
                className="flex-1 bg-[#161b22] border border-[#21262d] text-[#f0f6fc] text-sm rounded-xl px-3 py-2 placeholder-[#6e7681] focus:border-[#1f6feb] focus:outline-none transition-colors disabled:opacity-50"
              />
              <button
                onClick={() => submit(input)}
                disabled={!input.trim() || loading}
                className="bg-[#1f6feb] hover:bg-[#388bfd] disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl px-3 py-2 text-sm transition-colors"
              >
                →
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Pill trigger */}
      {!open && (
        <motion.button
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          onClick={() => setOpen(true)}
          className="relative flex items-center gap-2 bg-[#1f6feb] hover:bg-[#388bfd] text-white text-sm font-medium rounded-full px-4 py-3 shadow-lg transition-colors"
          style={{ boxShadow: "0 8px 32px rgba(31,111,235,0.25)" }}
        >
          {/* Live indicator */}
          <span className="relative flex w-2 h-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#3fb950] opacity-75" />
            <span className="relative inline-flex rounded-full w-2 h-2 bg-[#3fb950]" />
          </span>
          <span>✦ Ask CertifyIQ</span>
        </motion.button>
      )}
    </div>
  );
}