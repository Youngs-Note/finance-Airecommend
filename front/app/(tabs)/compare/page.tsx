"use client";

import type { ComparisonSummary, Product } from "@/lib/backend-api";
import RateChart from "@/components/rate-chart";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { useInView } from "react-intersection-observer";
import {
  fetchComparisonSummary,
  fetchFinancialProducts,
  fetchRateStats,
} from "./actions";
import type { RateStats } from "@/lib/backend-api";

export default function ComparePage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(false);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [summary, setSummary] = useState<ComparisonSummary | null>(null);
  const [summaryError, setSummaryError] = useState("");
  const [rateStats, setRateStats] = useState<RateStats[]>([]);

  // 💡 수정 1: rootMargin을 추가하여 바닥에 닿기 200px 전에 미리 감지하도록 설정
  const { ref, inView } = useInView({
    rootMargin: "200px",
  });

  const loadInitialProducts = useCallback(async (query: string) => {
    setLoading(true);
    const initialData = await fetchFinancialProducts(query, 0);
    setProducts(initialData);
    setPage(1);
    setHasMore(initialData.length === 10);
    setLoading(false);
  }, []);

  const loadMoreProducts = useCallback(async () => {
    if (loading || !hasMore) return;

    setLoading(true);
    const newData = await fetchFinancialProducts(searchQuery, page);

    if (newData.length === 0) {
      setHasMore(false);
    } else {
      setProducts((prev) => [...prev, ...newData]);
      setPage((prev) => prev + 1);
      if (newData.length < 10) setHasMore(false);
    }
    setLoading(false);
  }, [loading, hasMore, searchQuery, page]);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      loadInitialProducts(searchQuery);
    }, 500);

    return () => clearTimeout(delayDebounceFn);
  }, [searchQuery, loadInitialProducts]);

  useEffect(() => {
    if (inView && hasMore && !loading) {
      const timer = setTimeout(() => {
        void loadMoreProducts();
      }, 0);
      return () => clearTimeout(timer);
    }
  }, [inView, hasMore, loading, loadMoreProducts]);

  useEffect(() => {
    fetchRateStats().then(setRateStats).catch(() => setRateStats([]));
  }, []);

  return (
    <main className="w-full max-w-4xl mx-auto p-6 pb-24">
      <h1 className="text-3xl font-bold mb-8">금융 상품 비교</h1>

      <div className="relative mb-8">
        <input
          type="text"
          placeholder="은행명 또는 상품명을 입력하세요"
          className="w-full px-5 py-3 rounded-2xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {rateStats.length > 0 && (
        <section className="mb-8 rounded-2xl border border-gray-100 bg-white p-4 shadow-sm">
          <h2 className="mb-3 text-sm font-bold text-gray-800">
            예금·적금 평균 최고금리
          </h2>
          <RateChart stats={rateStats} />
        </section>
      )}

      <div className="grid gap-4">
        {products.map((product) => (
          <div
            key={product.id}
            className="p-5 bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow"
          >
            <div className="flex justify-between items-start gap-3">
              <Link href={`/compare/${encodeURIComponent(product.id)}`}>
                <span className="text-xs font-semibold text-green-600 bg-green-50 px-2 py-1 rounded-md">
                  {product.bank_name}
                </span>
                <h2 className="text-lg font-bold mt-2">
                  {product.product_name}
                </h2>
              </Link>
              <button
                type="button"
                onClick={() => {
                  setSummary(null);
                  setSummaryError("");
                  setSelectedIds((current) => {
                    if (current.includes(product.id)) {
                      return current.filter((id) => id !== product.id);
                    }
                    if (current.length >= 3) return current;
                    return [...current, product.id];
                  });
                }}
                className="shrink-0 text-sm font-medium text-gray-500 hover:text-green-600"
              >
                {selectedIds.includes(product.id) ? "비교해제" : "비교담기 +"}
              </button>
            </div>
          </div>
        ))}
      </div>

      {selectedIds.length > 0 && (
        <section className="mt-6 rounded-2xl border border-green-100 bg-green-50 p-4">
          <p className="text-sm text-green-800">
            비교 상품 {selectedIds.length}개 선택됨
          </p>
          <button
            type="button"
            disabled={selectedIds.length < 2}
            onClick={async () => {
              setSummaryError("");
              try {
                setSummary(await fetchComparisonSummary(selectedIds));
              } catch {
                setSummaryError("비교 요약을 불러오지 못했습니다.");
              }
            }}
            className="mt-3 rounded-xl bg-green-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
          >
            비교 요약 보기
          </button>
          {summaryError && (
            <p className="mt-3 text-sm text-red-500">{summaryError}</p>
          )}
          {summary && (
            <div className="mt-4 space-y-2 text-sm text-gray-700">
              <p>{summary.summary}</p>
              {summary.highlights.map((highlight) => (
                <p key={highlight}>- {highlight}</p>
              ))}
              <div className="flex justify-between items-start">
                <span className="text-xs text-gray-500">
                  규칙 기반 비교 요약
                </span>
              </div>
            </div>
          )}
        </section>
      )}

      {/* 💡 수정 3: 감지 영역에 위쪽 여백(mt-8)을 줘서 리스트와 간격 벌리기 */}
      <div ref={ref} className="h-20 flex items-center justify-center mt-8">
        {loading && (
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
        )}
        {!hasMore && products.length > 0 && (
          <p className="text-gray-400 text-sm">모든 상품을 불러왔습니다.</p>
        )}
        {!loading && products.length === 0 && (
          <p className="text-gray-400 text-sm">검색 결과가 없습니다.</p>
        )}
      </div>

      <p className="mt-4 text-xs leading-relaxed text-gray-400">
        금융상품통합비교공시시스템(금융감독원) 금융회사 상품정보를 사용한
        결과입니다. 가입 전 공식 상품 설명을 확인해 주세요.
      </p>
    </main>
  );
}
