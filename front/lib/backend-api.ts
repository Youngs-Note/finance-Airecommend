import "server-only";

const FASTAPI_BASE_URL =
  process.env.FASTAPI_BASE_URL ?? "http://127.0.0.1:8000";

export interface ProductOption {
  term_months: number;
  base_rate: number | null;
  max_rate: number | null;
  interest_type: string | null;
  saving_type: string | null;
}

export interface Product {
  id: string;
  source: "finlife" | "sample";
  product_type: "deposit" | "saving";
  bank_name: string;
  product_name: string;
  join_way: string[];
  join_member: string | null;
  special_conditions: string | null;
  maturity_interest: string | null;
  notes: string | null;
  options: ProductOption[];
}

export interface RecommendationResult {
  product: Product;
  score: number;
  reason_tags: string[];
  explanation: string;
  warnings: string[];
}

export interface ComparisonSummary {
  summary: string;
  highlights: string[];
  warnings: string[];
  ai_generated: boolean;
}

export interface RateStats {
  product_type: "deposit" | "saving";
  product_count: number;
  average_highest_rate: number;
  maximum_rate: number;
  minimum_rate: number;
}

export async function fetchBackend<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(`${FASTAPI_BASE_URL}${path}`, {
    cache: "no-store",
    ...options,
  });

  if (!response.ok) {
    throw new Error(`Backend request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}
