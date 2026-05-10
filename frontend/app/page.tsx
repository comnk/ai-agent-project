"use client";

import { useState } from "react";
import { QueryInput } from "@/components/QueryInput";
import { ReasoningTrace } from "@/components/ReasoningTrace";
import { runResearch } from "@/lib/api";
import { ResearchResponse } from "@/types/research";
import { SummaryCard } from "@/components/cards/SummaryCard";
import { ClaimCard } from "@/components/cards/ClaimCard";
import { ContradictionList } from "@/components/lists/ContradictionList";
import { SourcesList } from "@/components/lists/SourcesList";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ResearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (query: string) => {
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const data = await runResearch(query);
      setResult(data);
    } catch (e: any) {
      setError(e.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-zinc-50 dark:bg-zinc-950 transition-colors duration-300">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-8">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
            Veritas
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

        <ReasoningTrace
          trace={result?.execution_trace ?? []}
          loading={loading}
        />

        {result && (
          <div className="space-y-6">
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
