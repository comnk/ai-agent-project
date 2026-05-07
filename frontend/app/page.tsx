"use client";

import { useState } from "react";
import { QueryInput } from "@/components/QueryInput";
import { SummaryCard } from "@/components/cards/SummaryCard";
import { ClaimCard } from "@/components/cards/ClaimCard";
import { ResearchResponse, TraceStep } from "@/types/research";
import { ReasoningTrace } from "@/components/ReasoningTrace";
import { SourcesList } from "@/components/lists/SourcesList";
import { ContradictionList } from "@/components/lists/ContradictionList";
import { runResearch } from "@/lib/api";

const INITIAL_STEPS: TraceStep[] = [
  { label: "Planner Agent", detail: "", done: false },
  { label: "Research Agent", detail: "", done: false },
  { label: "Claim Extraction", detail: "", done: false },
  { label: "Verification", detail: "", done: false },
  { label: "Contradiction Detection", detail: "", done: false },
  { label: "ML Stance Analysis", detail: "", done: false },
  { label: "Writer Agent", detail: "", done: false },
];

function useSimulatedTrace() {
  const [steps, setSteps] = useState<TraceStep[]>([]);

  const start = () => {
    setSteps(INITIAL_STEPS.map((s) => ({ ...s, done: false })));
    const delays = [1200, 3000, 5000, 8000, 11000, 14000, 17000];
    delays.forEach((delay, idx) => {
      setTimeout(() => {
        setSteps((prev) =>
          prev.map((s, j) => (j === idx ? { ...s, done: true } : s)),
        );
      }, delay);
    });
  };

  const finish = (data: ResearchResponse) => {
    setSteps(
      INITIAL_STEPS.map((s, i) => ({
        ...s,
        done: true,
        detail: [
          `Created ${data.research_results?.length ?? 0} sub-questions`,
          `Analyzed ${data.all_sources?.length ?? 0} sources`,
          `Extracted ${data.extracted_claims?.length ?? 0} claims`,
          `${data.verification_summary?.SUPPORTED ?? 0} supported, ${data.verification_summary?.DISPUTED ?? 0} disputed`,
          `${data.contradictions?.length ?? 0} relationships detected`,
          `Avg confidence ${Math.round((data.verification_summary?.avg_confidence ?? 0) * 100)}%`,
          "Report generated",
        ][i],
      })),
    );
  };

  const reset = () => setSteps([]);

  return { steps, start, finish, reset };
}

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ResearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { steps, start, finish, reset } = useSimulatedTrace();

  const handleSubmit = async (query: string) => {
    setLoading(true);
    setResult(null);
    setError(null);
    reset();
    start();

    try {
      const data = await runResearch(query);
      finish(data);
      setResult(data);
    } catch (e: unknown) {
      setError((e as Error).message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-zinc-50 dark:bg-zinc-950 transition-colors duration-300">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-8">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
            AI Research Analyst
          </h1>
          <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
            Multi-agent research with claim verification and contradiction
            detection
          </p>
        </div>

        <QueryInput onSubmit={handleSubmit} loading={loading} />

        {error && (
          <div
            className="rounded-xl border border-red-200 dark:border-red-900/50 
                          bg-red-50 dark:bg-red-950/30 px-5 py-4"
          >
            <p className="text-sm text-red-700 dark:text-red-400">{error}</p>
          </div>
        )}

        <ReasoningTrace steps={steps} loading={loading} />

        {result && (
          <div className="space-y-6 animate-in fade-in duration-500">
            <SummaryCard
              answer={result.answer}
              summary={result.verification_summary}
            />

            {result.verifications && result.verifications.length > 0 && (
              <div>
                <h2 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 mb-3">
                  Key Claims
                  <span className="ml-2 text-xs font-normal text-zinc-400 dark:text-zinc-500">
                    {result.verifications.length} total
                  </span>
                </h2>
                <div className="space-y-3">
                  {result.verifications.map((v, i) => (
                    <ClaimCard key={i} verification={v} />
                  ))}
                </div>
              </div>
            )}

            <ContradictionList contradictions={result.contradictions} />

            <SourcesList sources={result.all_sources} />

            <p className="text-xs text-zinc-400 dark:text-zinc-600 text-center">
              Session {result.session_id.slice(0, 8)} · {result.claims_stored}{" "}
              claims stored
            </p>
          </div>
        )}
      </div>
    </main>
  );
}
