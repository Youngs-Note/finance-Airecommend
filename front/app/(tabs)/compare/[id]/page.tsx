"use client";

import type { Product } from "@/lib/backend-api";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import fetchProductDetails from "./actions";

export default function ProductDetailPage() {
  const params = useParams();
  const productId = params.id as string;
  const [product, setProduct] = useState<Product | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (productId) {
      fetchProductDetails(productId)
        .then((data) => {
          setProduct(data);
        })
        .catch((err) => {
          console.error("Failed to fetch product details:", err);
          setError("상품 상세 정보를 불러오는 데 실패했습니다.");
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [productId]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center flex-1 h-full min-h-[60vh] space-y-4">
        {/* 회전하는 스피너 (Spinning Circle) */}
        <div className="w-12 h-12 rounded-full border-4 border-gray-100 border-t-green-600 animate-spin"></div>
      </div>
    );
  }

  if (error) {
    return <p className="text-red-500 text-center mt-10">{error}</p>;
  }

  if (!product) {
    return (
      <p className="text-gray-500 text-center mt-10">
        상품을 찾을 수 없습니다.
      </p>
    );
  }

  return (
    <main className="max-w-4xl mx-auto p-6 pb-24">
      <h1 className="text-3xl font-bold mb-4">{product.product_name}</h1>
      <p className="text-green-600 text-xl mb-6">{product.bank_name}</p>

      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 mb-8">
        <h2 className="text-xl font-semibold mb-3">상품 상세</h2>
        <p className="text-gray-700 leading-relaxed">
          {product.special_conditions || "별도 우대조건 안내가 없습니다."}
        </p>
        <div className="mt-4 text-gray-600">
          <p>
            <strong>가입 방식:</strong>{" "}
            {product.join_way.join(", ") || "공식 상품 설명을 확인해 주세요."}
          </p>
          <br />
          <p>
            <strong>상품 유형:</strong>{" "}
            {product.product_type === "deposit" ? "예금" : "적금"}
          </p>
          <div className="mt-4 space-y-2">
            {product.options.map((option) => (
              <p key={`${option.term_months}-${option.interest_type}`}>
                <strong>{option.term_months}개월:</strong> 기본{" "}
                {option.base_rate ?? "-"}%, 최고 {option.max_rate ?? "-"}%
              </p>
            ))}
          </div>
        </div>
      </div>

      <p className="mb-6 text-xs leading-relaxed text-gray-400">
        금융상품통합비교공시시스템(금융감독원) 금융회사 상품정보를 사용한
        결과입니다. 가입 전 공식 상품 설명을 확인해 주세요.
      </p>

      <Link
        href={"/compare"}
        className="px-6 py-3 bg-gray-200 text-gray-800 rounded-xl hover:bg-gray-300 transition-colors"
      >
        {"목록으로 돌아가기"}
      </Link>
    </main>
  );
}
