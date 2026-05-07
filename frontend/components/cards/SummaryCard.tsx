"use client";

import { VerificationSummary } from "@/types/research";

interface Props {
  answer: string;
  summary: VerificationSummary;
}

function ConfidenceBar({ value }: { value: number }) {
  const pct = Math.round(value * 100);
  const color =
    pct >= 75 ? "bg-emerald-500" : pct >= 50 ? "bg-amber-500" : "bg-red-500";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 rounded-full bg-zinc-200 dark:bg-zinc-700">
        <div
          className={`h-full rounded-full ${color} transition-all duration-700`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-xs font-mono text-zinc-500 dark:text-zinc-400 w-8">
        {pct}%
      </span>
    </div>
  );
}

export function SummaryCard({ answer, summary }: Props) {
  // Parse sections from the answer string
  const sections = answer.split(/\n(?=[A-Z\s]+:)/);
  const execSummary =
    sections
      .find((s) => s.startsWith("EXECUTIVE SUMMARY"))
      ?.replace("EXECUTIVE SUMMARY:\n", "")
      .trim() || answer;

  return (
    <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 overflow-hidden">
      {/* Header */}
      <div
        className="px-5 py-4 border-b border-zinc-200 dark:border-zinc-800 
                      bg-white dark:bg-zinc-900 flex items-center justify-between"
      >
        <h2 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
          Executive Summary
        </h2>
        <div className="flex items-center gap-4 text-xs">
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <span className="text-zinc-500 dark:text-zinc-400">
              {summary.SUPPORTED} supported
            </span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-amber-500" />
            <span className="text-zinc-500 dark:text-zinc-400">
              {summary.DISPUTED} disputed
            </span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-zinc-400" />
            <span className="text-zinc-500 dark:text-zinc-400">
              {summary.UNCERTAIN} uncertain
            </span>
          </span>
        </div>
      </div>

      {/* Body */}
      <div className="p-5 bg-white dark:bg-zinc-900">
        <p className="text-sm leading-relaxed text-zinc-700 dark:text-zinc-300">
          {execSummary}
        </p>

        <div className="mt-5 pt-5 border-t border-zinc-100 dark:border-zinc-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-zinc-500 dark:text-zinc-400">
              Average confidence
            </span>
          </div>
          <ConfidenceBar value={summary.avg_confidence} />
        </div>
      </div>
    </div>
  );
}
