from types import SimpleNamespace
from typing import Any

from backend.app.core.config import Settings
from backend.app.data.sample_products import get_sample_products
from backend.app.schemas.ai import AIProductExplanation, AIRecommendationExplanations
from backend.app.schemas.product import ProductType
from backend.app.schemas.recommendation import RecommendationRequest
from backend.app.services.ai_explainer import AIExplainer
from backend.app.services.recommender import recommend_products


class FakeResponses:
    def __init__(self, parsed: Any) -> None:
        self.parsed = parsed

    def parse(self, **_kwargs: Any) -> SimpleNamespace:
        return SimpleNamespace(output_parsed=self.parsed)


class FakeOpenAI:
    def __init__(self, parsed: Any) -> None:
        self.responses = FakeResponses(parsed)


def _recommendation_results():
    request = RecommendationRequest(
        product_type=ProductType.DEPOSIT,
        term_months=12,
        max_results=1,
    )
    products = [
        product for product in get_sample_products() if product.product_type == ProductType.DEPOSIT
    ]
    return request, recommend_products(products, request)


def test_ai_explainer_keeps_fallback_when_disabled() -> None:
    request, results = _recommendation_results()
    explainer = AIExplainer(Settings())

    enhanced = explainer.enhance_recommendations(results, request)

    assert enhanced == results


def test_ai_explainer_applies_valid_structured_summary() -> None:
    request, results = _recommendation_results()
    parsed = AIRecommendationExplanations(
        items=[
            AIProductExplanation(
                product_id=results[0].product.id,
                summary="입력 조건과 우대조건을 함께 살펴볼 만한 상품입니다.",
                warnings=["공식 설명에서 적용 조건을 확인해 주세요."],
            )
        ]
    )
    explainer = AIExplainer(
        Settings(openai_explanations_enabled=True, openai_api_key="test-key"),
        client=FakeOpenAI(parsed),
    )

    enhanced = explainer.enhance_recommendations(results, request)

    assert enhanced[0].explanation == parsed.items[0].summary
    assert parsed.items[0].warnings[0] in enhanced[0].warnings


def test_ai_explainer_rejects_numeric_claim_and_uses_fallback() -> None:
    request, results = _recommendation_results()
    parsed = AIRecommendationExplanations(
        items=[
            AIProductExplanation(
                product_id=results[0].product.id,
                summary="우대금리가 9%인 상품입니다.",
            )
        ]
    )
    explainer = AIExplainer(
        Settings(openai_explanations_enabled=True, openai_api_key="test-key"),
        client=FakeOpenAI(parsed),
    )

    enhanced = explainer.enhance_recommendations(results, request)

    assert enhanced == results


def test_ai_explainer_keeps_fallback_when_parsed_output_is_missing() -> None:
    request, results = _recommendation_results()
    explainer = AIExplainer(
        Settings(openai_explanations_enabled=True, openai_api_key="test-key"),
        client=FakeOpenAI(None),
    )

    enhanced = explainer.enhance_recommendations(results, request)

    assert enhanced == results


def test_ai_explainer_rejects_prohibited_phrase_and_uses_fallback() -> None:
    request, results = _recommendation_results()
    parsed = AIRecommendationExplanations(
        items=[
            AIProductExplanation(
                product_id=results[0].product.id,
                summary="반드시 가입해야 하는 상품입니다.",
            )
        ]
    )
    explainer = AIExplainer(
        Settings(openai_explanations_enabled=True, openai_api_key="test-key"),
        client=FakeOpenAI(parsed),
    )

    enhanced = explainer.enhance_recommendations(results, request)

    assert enhanced == results
