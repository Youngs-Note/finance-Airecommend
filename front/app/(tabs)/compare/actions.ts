"use server";

const PAGE_SIZE = 10; // 한 번에 가져올 상품 개수

import {
  fetchBackend,
  type ComparisonSummary,
  type Product,
  type RateStats,
} from "@/lib/backend-api";

export async function fetchFinancialProducts(
  query: string,
  page: number,
): Promise<Product[]> {
  try {
    const products = await fetchBackend<Product[]>("/api/products");
    const normalizedQuery = query.trim().toLocaleLowerCase("ko-KR");
    return products
      .filter((product) => {
        if (!normalizedQuery) return true;
        return [product.bank_name, product.product_name].some((value) =>
          value.toLocaleLowerCase("ko-KR").includes(normalizedQuery),
        );
      })
      .slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);
  } catch (error) {
    console.error("상품 불러오기 에러:", error);
    return [];
  }
}

export async function fetchComparisonSummary(
  productIds: string[],
): Promise<ComparisonSummary> {
  return fetchBackend<ComparisonSummary>("/api/products/compare-summary", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_ids: productIds }),
  });
}

export async function fetchRateStats(): Promise<RateStats[]> {
  return fetchBackend<RateStats[]>("/api/stats/rates");
}
