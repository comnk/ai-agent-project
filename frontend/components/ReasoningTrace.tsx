"use client";

import { useEffect, useState } from "react";

interface TraceEvent {
  agent: string;
  action: string;
  details: Record<string, any>;
  timestamp: string;
}

interface Props {
  trace: TraceEvent[];
  loading: boolean;
}

const AGENT_META: Record<string, { label: string; color: string }> = {
  planner_agent: { label: "Planner Agent", color: "bg-violet-500" },
  research_agent: { label: "Research Agent", color: "bg-blue-500" },
  claim_extractor_agent: { label: "Claim Extraction", color: "bg-cyan-500" },
  verification_agent: { label: "Verification", color: "bg-amber-500" },
  contradiction_agent: {
    label: "Contradiction Detection",
    color: "bg-orange-500",
  },
  ml_layer: { label: "ML Stance Analysis", color: "bg-pink-500" },
  writer_agent: { label: "Writer Agent", color: "bg-emerald-500" },
};

const AGENT_ORDER = [
  "planner_agent",
  "research_agent",
  "claim_extractor_agent",
  "verification_agent",
  "contradiction_agent",
  "ml_layer",
  "writer_agent",
];

const STEP_REVEAL_DELAYS = [1500, 5000, 9000, 13000, 16000, 19000, 22000];

function formatDetails(action: string, details: Record<string, any>): string {
  switch (action) {
    case "sub_questions_created":
      return `Created ${details.count} sub-question${details.count !== 1 ? "s" : ""}`;
    case "sources_gathered":
      return `Gathered ${details.source_count} source${details.source_count !== 1 ? "s" : ""} across ${details.sub_questions} queries`;
    case "claims_extracted":
      return `Extracted ${details.claim_count} claims across ${details.topics?.length ?? 0} topics`;
    case "claims_verified":
      return `${details.supported} supported · ${details.disputed} disputed · ${details.uncertain} uncertain`;
    case "contradictions_detected":
      return `${details.conflicts} conflict${details.conflicts !== 1 ? "s" : ""} across ${details.topic_clusters} topic clusters`;
    case "stance_analysis_complete":
      return `Analyzed ${details.claims_analyzed} claims · avg confidence ${Math.round((details.avg_ml_confidence ?? 0) * 100)}%`;
    case "report_generated":
      return `${details.claims_stored} claims stored · ${details.duplicates_removed ?? 0} duplicates removed`;
    default:
      return action.replace(/_/g, " ");
  }
}

export function ReasoningTrace({ trace, loading }: Props) {
  const [revealedCount, setRevealedCount] = useState(0);

  useEffect(() => {
    if (!loading) {
      setRevealedCount(0);
      return;
    }

    const timers = STEP_REVEAL_DELAYS.map((delay, i) =>
      setTimeout(() => setRevealedCount(i + 1), delay),
    );
    return () => timers.forEach(clearTimeout);
  }, [loading]);

  const showTrace = !loading && trace.length > 0;
  const showSkeleton = loading;

  if (!showTrace && !showSkeleton) return null;

  return (
    <div
      className="rounded-xl border border-zinc-200 dark:border-zinc-800
                    bg-zinc-50 dark:bg-zinc-900/50 p-5"
    >
      <h2 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-4">
        Reasoning Trace
      </h2>

      <div className="space-y-3">
        {showSkeleton
          ? AGENT_ORDER.map((agent, i) => {
              const meta = AGENT_META[agent];
              const done = i < revealedCount;
              return (
                <div key={i} className="flex items-start gap-3">
                  <div
                    className={`mt-0.5 w-5 h-5 rounded-full shrink-0 flex items-center justify-center
                                  transition-all duration-500
                                  ${done ? meta.color : "bg-zinc-200 dark:bg-zinc-700"}`}
                  >
                    {done && (
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
                  <p
                    className={`text-sm font-medium transition-colors duration-300
                                ${done ? "text-zinc-900 dark:text-zinc-100" : "text-zinc-300 dark:text-zinc-600"}`}
                  >
                    {meta.label}
                  </p>
                </div>
              );
            })
          : trace.map((event, i) => {
              const meta = AGENT_META[event.agent] ?? {
                label: event.agent,
                color: "bg-zinc-500",
              };
              return (
                <div key={i} className="flex items-start gap-3">
                  <div
                    className={`mt-0.5 w-5 h-5 rounded-full ${meta.color} flex items-center justify-center shrink-0`}
                  >
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
                  </div>
                  <div>
                    <p className="text-sm font-medium text-zinc-900 dark:text-zinc-100">
                      {meta.label}
                    </p>
                    <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
                      {formatDetails(event.action, event.details)}
                    </p>
                  </div>
                </div>
              );
            })}

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
              Pipeline running...
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
