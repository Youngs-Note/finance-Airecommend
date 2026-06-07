"use server";

import {
  fetchBackend,
  type RecommendationResult,
} from "@/lib/backend-api";

export async function fetchRecommendations(
  productType: "deposit" | "saving",
  termMonths: number,
): Promise<RecommendationResult[]> {
  return fetchBackend<RecommendationResult[]>("/api/recommendations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      product_type: productType,
      term_months: termMonths,
      max_results: 3,
    }),
  });
}
