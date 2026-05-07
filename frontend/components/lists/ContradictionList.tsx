"use client";

import { Contradiction } from "@/types/research";
import { useState } from "react";

interface Props {
  contradictions: Contradiction[];
}

function ContradictionItem({ c }: { c: Contradiction }) {
  const [open, setOpen] = useState(false);
  const isContra = c.relation === "CONTRADICTS";

  return (
    <div
      className={`rounded-xl border overflow-hidden transition-all duration-200
                     ${
                       isContra
                         ? "border-red-200 dark:border-red-900/50"
                         : "border-zinc-200 dark:border-zinc-800"
                     }`}
    >
      <button
        onClick={() => setOpen((o) => !o)}
        className="w-full px-4 py-3 flex items-center justify-between text-left
                   bg-white dark:bg-zinc-900 hover:bg-zinc-50 dark:hover:bg-zinc-800/50
                   transition-colors duration-150"
      >
        <div className="flex items-center gap-3 min-w-0">
          <span
            className={`shrink-0 text-xs font-semibold px-2 py-0.5 rounded
                           ${
                             isContra
                               ? "bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-400"
                               : "bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400"
                           }`}
          >
            {c.relation}
          </span>
          <span className="text-xs text-zinc-500 dark:text-zinc-400 truncate">
            {c.topic}
          </span>
        </div>
        <svg
          className={`w-4 h-4 text-zinc-400 shrink-0 transition-transform duration-200 ${open ? "rotate-180" : ""}`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {open && (
        <div className="px-4 pb-4 bg-white dark:bg-zinc-900 border-t border-zinc-100 dark:border-zinc-800">
          <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="rounded-lg bg-zinc-50 dark:bg-zinc-800/50 p-3">
              <p className="text-xs font-medium text-zinc-400 dark:text-zinc-500 mb-1">
                Claim A
              </p>
              <p className="text-sm text-zinc-800 dark:text-zinc-200">
                {c.claim_a}
              </p>
            </div>
            <div className="rounded-lg bg-zinc-50 dark:bg-zinc-800/50 p-3">
              <p className="text-xs font-medium text-zinc-400 dark:text-zinc-500 mb-1">
                Claim B
              </p>
              <p className="text-sm text-zinc-800 dark:text-zinc-200">
                {c.claim_b}
              </p>
            </div>
          </div>
          <p className="mt-3 text-xs text-zinc-500 dark:text-zinc-400 italic">
            {c.explanation}
          </p>
        </div>
      )}
    </div>
  );
}

export function ContradictionList({ contradictions }: Props) {
  if (!contradictions || contradictions.length === 0) return null;

  const conflicts = contradictions.filter((c) => c.relation === "CONTRADICTS");
  const supports = contradictions.filter((c) => c.relation === "SUPPORTS");

  return (
    <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 overflow-hidden">
      <div
        className="px-5 py-4 border-b border-zinc-200 dark:border-zinc-800
                      bg-white dark:bg-zinc-900 flex items-center justify-between"
      >
        <h2 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
          Claim Relationships
        </h2>
        <div className="flex items-center gap-3 text-xs">
          {conflicts.length > 0 && (
            <span className="bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-400 px-2 py-0.5 rounded-full">
              {conflicts.length} conflict{conflicts.length !== 1 ? "s" : ""}
            </span>
          )}
          {supports.length > 0 && (
            <span className="bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400 px-2 py-0.5 rounded-full">
              {supports.length} supporting
            </span>
          )}
        </div>
      </div>
      <div className="p-4 bg-zinc-50 dark:bg-zinc-900/30 space-y-2">
        {[...conflicts, ...supports].map((c, i) => (
          <ContradictionItem key={i} c={c} />
        ))}
      </div>
    </div>
  );
}
