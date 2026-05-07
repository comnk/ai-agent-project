"use client";

import { TraceStep } from "@/types/research";

interface Props {
  steps: TraceStep[];
  loading: boolean;
}

export function ReasoningTrace({ steps, loading }: Props) {
  if (steps.length === 0 && !loading) return null;

  return (
    <div
      className="rounded-xl border border-zinc-200 dark:border-zinc-800 
                    bg-zinc-50 dark:bg-zinc-900/50 p-5"
    >
      <h2 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-4">
        Reasoning Trace
      </h2>
      <div className="space-y-3">
        {steps.map((step, i) => (
          <div key={i} className="flex items-start gap-3">
            <div
              className={`mt-0.5 w-5 h-5 rounded-full flex items-center justify-center shrink-0
                            transition-all duration-300
                            ${
                              step.done
                                ? "bg-indigo-600 dark:bg-indigo-500"
                                : "bg-zinc-200 dark:bg-zinc-700 animate-pulse"
                            }`}
            >
              {step.done && (
                <svg
                  className="w-3 h-3 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2.5}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              )}
            </div>
            <div>
              <p
                className={`text-sm font-medium transition-colors duration-300
                            ${
                              step.done
                                ? "text-zinc-900 dark:text-zinc-100"
                                : "text-zinc-400 dark:text-zinc-500"
                            }`}
              >
                {step.label}
              </p>
              {step.done && step.detail && (
                <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
                  {step.detail}
                </p>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-2 pt-1">
            <div className="flex gap-1">
              {[0, 1, 2].map((i) => (
                <div
                  key={i}
                  className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-bounce"
                  style={{ animationDelay: `${i * 0.15}s` }}
                />
              ))}
            </div>
            <span className="text-xs text-zinc-400 dark:text-zinc-500">
              Processing...
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
