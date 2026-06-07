import json
import logging
import re
from typing import Any

from openai import OpenAI

from backend.app.core.config import Settings
from backend.app.schemas.ai import (
    AIComparisonSummary,
    AIRecommendationExplanations,
    ComparisonSummary,
)
from backend.app.schemas.product import Product
from backend.app.schemas.recommendation import RecommendationRequest, RecommendationResult

logger = logging.getLogger(__name__)

FORBIDDEN_PHRASES = (
    "무조건",
    "반드시 가입",
    "수익을 보장",
    "최고의 상품",
)
OFFICIAL_PRODUCT_WARNING = "가입 전 공식 상품 설명과 우대조건을 확인해야 합니다."


class AIExplainer:
    def __init__(self, settings: Settings, client: Any | None = None) -> None:
        self.settings = settings
        self.client = client
        if client is None and self.enabled:
            self.client = OpenAI(
                api_key=settings.openai_api_key,
                timeout=settings.openai_timeout_seconds,
                max_retries=1,
            )

    @property
    def enabled(self) -> bool:
        return self.settings.openai_explanations_enabled and bool(self.settings.openai_api_key)

    def enhance_recommendations(
        self,
        results: list[RecommendationResult],
        request: RecommendationRequest,
    ) -> list[RecommendationResult]:
        if not self.enabled or self.client is None or not results:
            return results

        try:
            response = self.client.responses.parse(
                model=self.settings.openai_model,
                input=[
                    {"role": "system", "content": _recommendation_system_prompt()},
                    {
                        "role": "user",
                        "content": json.dumps(
                            _recommendation_payload(results, request),
                            ensure_ascii=False,
                        ),
                    },
                ],
                text_format=AIRecommendationExplanations,
            )
            parsed = response.output_parsed
            if parsed is None:
                return results
            return _apply_ai_explanations(results, parsed)
        except Exception as exc:  # noqa: BLE001 - fallback is required for API failures.
            logger.warning("OpenAI recommendation explanation fallback: %s", type(exc).__name__)
            return results

    def summarize_comparison(self, products: list[Product]) -> ComparisonSummary:
        fallback = _fallback_comparison_summary(products)
        if not self.enabled or self.client is None:
            return fallback

        try:
            response = self.client.responses.parse(
                model=self.settings.openai_model,
                input=[
                    {"role": "system", "content": _comparison_system_prompt()},
                    {
                        "role": "user",
                        "content": json.dumps(
                            {"products": [_product_payload(product) for product in products]},
                            ensure_ascii=False,
                        ),
                    },
                ],
                text_format=AIComparisonSummary,
            )
            parsed = response.output_parsed
            if parsed is None:
                return fallback
            _validate_generated_text([parsed.summary, *parsed.highlights, *parsed.warnings])
            return ComparisonSummary(
                summary=parsed.summary,
                highlights=parsed.highlights,
                warnings=[OFFICIAL_PRODUCT_WARNING, *parsed.warnings],
                ai_generated=True,
            )
        except Exception as exc:  # noqa: BLE001 - fallback is required for API failures.
            logger.warning("OpenAI comparison summary fallback: %s", type(exc).__name__)
            return fallback


def _recommendation_system_prompt() -> str:
    return (
        "당신은 예금과 적금 비교 서비스의 설명 보조자입니다. 제공된 후보의 추천 이유를 "
        "간결한 한국어로 다시 설명하세요. 새로운 상품, 은행, 금리, 기간, 수치 또는 조건을 "
        "추가하지 마세요. 숫자와 퍼센트 기호를 출력하지 마세요. 가입을 단정하거나 수익을 "
        "보장하지 마세요. 각 product_id는 입력값을 그대로 사용하세요."
    )


def _comparison_system_prompt() -> str:
    return (
        "당신은 예금과 적금 비교 서비스의 설명 보조자입니다. 제공된 상품만 비교하여 간결한 "
        "한국어 요약을 만드세요. 새로운 상품, 은행, 금리, 기간, 수치 또는 조건을 추가하지 "
        "마세요. 숫자와 퍼센트 기호를 출력하지 마세요. 가입을 단정하거나 수익을 보장하지 "
        "마세요."
    )


def _recommendation_payload(
    results: list[RecommendationResult],
    request: RecommendationRequest,
) -> dict[str, Any]:
    return {
        "selected_product_type": request.product_type,
        "candidates": [
            {
                **_product_payload(result.product),
                "product_id": result.product.id,
                "reason_tags": result.reason_tags,
            }
            for result in results
        ],
    }


def _product_payload(product: Product) -> dict[str, Any]:
    return {
        "product_id": product.id,
        "product_type": product.product_type,
        "bank_name": product.bank_name,
        "product_name": product.product_name,
        "join_way": product.join_way,
        "special_conditions": product.special_conditions,
    }


def _apply_ai_explanations(
    results: list[RecommendationResult],
    parsed: AIRecommendationExplanations,
) -> list[RecommendationResult]:
    result_by_id = {result.product.id: result for result in results}
    explanation_by_id = {}

    for item in parsed.items:
        if item.product_id not in result_by_id or item.product_id in explanation_by_id:
            raise ValueError("OpenAI returned an unknown or duplicate product ID.")
        _validate_generated_text([item.summary, *item.warnings])
        explanation_by_id[item.product_id] = item

    return [
        (
            result.model_copy(
                update={
                    "explanation": explanation_by_id[result.product.id].summary,
                    "warnings": [*result.warnings, *explanation_by_id[result.product.id].warnings],
                }
            )
            if result.product.id in explanation_by_id
            else result
        )
        for result in results
    ]


def _fallback_comparison_summary(products: list[Product]) -> ComparisonSummary:
    product_names = ", ".join(product.product_name for product in products)
    return ComparisonSummary(
        summary=f"{product_names}의 공식 상품 조건을 나란히 확인해 주세요.",
        highlights=["가입 방식과 우대조건을 함께 비교해 주세요."],
        warnings=[OFFICIAL_PRODUCT_WARNING],
    )


def _validate_generated_text(texts: list[str]) -> None:
    combined = " ".join(texts)
    if re.search(r"[\d%]", combined):
        raise ValueError("OpenAI explanation introduced a numeric claim.")
    if any(phrase in combined for phrase in FORBIDDEN_PHRASES):
        raise ValueError("OpenAI explanation used a prohibited phrase.")
