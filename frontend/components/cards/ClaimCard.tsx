"use client";

import { Verification } from "@/types/research";

interface Props {
  verification: Verification;
}

const STATUS_STYLES = {
  SUPPORTED: {
    badge:
      "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-400",
    border: "border-l-emerald-500",
    dot: "bg-emerald-500",
  },
  DISPUTED: {
    badge:
      "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-400",
    border: "border-l-amber-500",
    dot: "bg-amber-500",
  },
  UNCERTAIN: {
    badge: "bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400",
    border: "border-l-zinc-400",
    dot: "bg-zinc-400",
  },
};

const STANCE_STYLES = {
  SUPPORTS: "text-emerald-600 dark:text-emerald-400",
  OPPOSES: "text-red-600 dark:text-red-400",
  NEUTRAL: "text-zinc-500 dark:text-zinc-400",
};

export function ClaimCard({ verification: v }: Props) {
  const style = STATUS_STYLES[v.status] || STATUS_STYLES.UNCERTAIN;
  const pct = Math.round(v.confidence * 100);
  const barColor =
    pct >= 75 ? "bg-emerald-500" : pct >= 50 ? "bg-amber-500" : "bg-red-500";

  return (
    <div
      className={`rounded-xl border border-zinc-200 dark:border-zinc-800 border-l-4 ${style.border}
                     bg-white dark:bg-zinc-900 p-4 transition-all duration-200
                     hover:shadow-md dark:hover:shadow-zinc-900`}
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <p className="text-sm text-zinc-800 dark:text-zinc-200 leading-snug flex-1">
          {v.claim}
        </p>
        <span
          className={`shrink-0 text-xs font-medium px-2.5 py-1 rounded-full ${style.badge}`}
        >
          {v.status}
        </span>
      </div>

      <div className="mb-3">
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs text-zinc-400 dark:text-zinc-500">
            Confidence
          </span>
          <span className="text-xs font-mono text-zinc-600 dark:text-zinc-400">
            {pct}%
          </span>
        </div>
        <div className="h-1.5 rounded-full bg-zinc-100 dark:bg-zinc-800">
          <div
            className={`h-full rounded-full ${barColor} transition-all duration-700`}
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className="text-zinc-400 dark:text-zinc-500">{v.reason}</span>
        {v.ml_stance && (
          <span
            className={`font-medium shrink-0 ml-3 ${STANCE_STYLES[v.ml_stance]}`}
          >
            ML: {v.ml_stance}
          </span>
        )}
      </div>

      {(v.supporting_evidence?.length > 0 ||
        v.contradicting_evidence?.length > 0) && (
        <div className="mt-3 pt-3 border-t border-zinc-100 dark:border-zinc-800 space-y-1.5">
          {v.supporting_evidence?.map((e, i) => (
            <p
              key={i}
              className="text-xs text-zinc-500 dark:text-zinc-400 flex gap-2"
            >
              <span className="text-emerald-500 shrink-0">+</span>
              {e}
            </p>
          ))}
          {v.contradicting_evidence?.map((e, i) => (
            <p
              key={i}
              className="text-xs text-zinc-500 dark:text-zinc-400 flex gap-2"
            >
              <span className="text-red-500 shrink-0">−</span>
              {e}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}
