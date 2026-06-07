"use client";

import type { RecommendationResult } from "@/lib/backend-api";
import { useState } from "react";
import { fetchRecommendations } from "./actions";

export default function RecommendPage() {
  const [productType, setProductType] = useState<"deposit" | "saving">(
    "deposit",
  );
  const [termMonths, setTermMonths] = useState(12);
  const [results, setResults] = useState<RecommendationResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      setResults(await fetchRecommendations(productType, termMonths));
    } catch {
      setError("추천 결과를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="w-full p-6 pb-24">
      <h1 className="text-3xl font-bold mb-2">AI 추천</h1>
      <p className="text-sm text-gray-500 mb-6">
        선택한 조건 기준으로 우선 확인할 상품을 안내합니다.
      </p>

      <form
        onSubmit={handleSubmit}
        className="space-y-4 rounded-2xl border border-gray-100 bg-white p-5 shadow-sm"
      >
        <label className="block">
          <span className="text-sm font-semibold text-gray-700">상품 유형</span>
          <select
            value={productType}
            onChange={(event) =>
              setProductType(event.target.value as "deposit" | "saving")
            }
            className="mt-2 w-full rounded-xl border border-gray-200 px-4 py-3"
          >
            <option value="deposit">예금</option>
            <option value="saving">적금</option>
          </select>
        </label>

        <label className="block">
          <span className="text-sm font-semibold text-gray-700">가입 기간</span>
          <select
            value={termMonths}
            onChange={(event) => setTermMonths(Number(event.target.value))}
            className="mt-2 w-full rounded-xl border border-gray-200 px-4 py-3"
          >
            <option value={6}>6개월</option>
            <option value={12}>12개월</option>
            <option value={24}>24개월</option>
          </select>
        </label>

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-xl bg-green-600 px-4 py-3 font-semibold text-white hover:bg-green-700 disabled:opacity-60"
        >
          {loading ? "분석 중..." : "추천 결과 보기"}
        </button>
      </form>

      {error && <p className="mt-4 text-sm text-red-500">{error}</p>}

      <div className="mt-6 space-y-4">
        {results.map((result) => (
          <article
            key={result.product.id}
            className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm"
          >
            <p className="text-xs font-semibold text-green-600">
              {result.product.bank_name}
            </p>
            <h2 className="mt-1 text-lg font-bold">
              {result.product.product_name}
            </h2>
            <p className="mt-3 text-sm text-gray-700">{result.explanation}</p>
            <p className="mt-3 text-sm font-semibold text-green-700">
              조건 적합도 {result.score.toFixed(1)}점
            </p>
            <div className="mt-3 flex flex-wrap gap-2">
              {result.reason_tags.map((tag) => (
                <span
                  key={tag}
                  className="rounded-full bg-green-50 px-3 py-1 text-xs text-green-700"
                >
                  {tag}
                </span>
              ))}
            </div>
          </article>
        ))}
      </div>

      <p className="mt-6 text-xs text-gray-400 leading-relaxed">
        추천 순위는 규칙 기반 점수로 계산합니다. 가입 전 공식 상품 설명과
        우대조건을 확인해 주세요.
      </p>
    </main>
  );
}
