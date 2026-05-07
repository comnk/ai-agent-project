export interface ResearchResult {
  question: string;
  summary: string;
  sources: string[];
  confidence: number;
}

export interface Verification {
  claim_id: string;
  claim: string;
  status: "SUPPORTED" | "DISPUTED" | "UNCERTAIN";
  supporting_evidence: string[];
  contradicting_evidence: string[];
  confidence: number;
  reason: string;
  ml_stance: "SUPPORTS" | "OPPOSES" | "NEUTRAL";
  ml_stance_confidence: number;
  ml_similarity: number;
  ml_confidence: number;
}

export interface Contradiction {
  claim_a: string;
  claim_b: string;
  topic: string;
  relation: "CONTRADICTS" | "SUPPORTS" | "UNRELATED";
  explanation: string;
}

export interface VerificationSummary {
  SUPPORTED: number;
  DISPUTED: number;
  UNCERTAIN: number;
  avg_confidence: number;
  total_claims: number;
  ml_stance_counts: {
    SUPPORTS: number;
    OPPOSES: number;
    NEUTRAL: number;
  };
}

export interface ResearchResponse {
  answer: string;
  research_results: ResearchResult[];
  extracted_claims: any[];
  verifications: Verification[];
  contradictions: Contradiction[];
  topic_clusters: Record<string, string[]>;
  ml_candidate_pairs: any[];
  verification_summary: VerificationSummary;
  claims_stored: number;
  similar_past_claims: any[];
  all_sources: string[];
  session_id: string;
}

export interface TraceStep {
  label: string;
  detail: string;
  done: boolean;
}