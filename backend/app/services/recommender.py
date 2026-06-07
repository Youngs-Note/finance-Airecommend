from backend.app.schemas.product import Product, ProductOption
from backend.app.schemas.recommendation import RecommendationRequest, RecommendationResult


def recommend_products(
    products: list[Product],
    request: RecommendationRequest,
) -> list[RecommendationResult]:
    results = [
        _score_product(product, request)
        for product in products
        if product.product_type == request.product_type
    ]
    return sorted(results, key=lambda result: result.score, reverse=True)[: request.max_results]


def _score_product(product: Product, request: RecommendationRequest) -> RecommendationResult:
    option = _select_option(product, request.term_months)
    score = 0.0
    reason_tags: list[str] = []
    warnings = ["가입 전 공식 상품 설명과 우대조건을 확인해야 합니다."]

    if option is not None:
        score += 30
        reason_tags.append(f"{request.term_months}개월 조건 일치")
        if option.max_rate is not None:
            score += min(option.max_rate * 10, 40)
            reason_tags.append("우대금리 확인 가능")
        elif option.base_rate is not None:
            score += min(option.base_rate * 10, 35)
            reason_tags.append("기본금리 확인 가능")
    else:
        warnings.append("선택한 가입기간과 정확히 일치하는 옵션이 없습니다.")

    if request.prefer_simple_conditions:
        condition_length = len(product.special_conditions or "")
        if condition_length <= 80:
            score += 20
            reason_tags.append("비교적 단순한 우대조건")
        else:
            warnings.append("우대조건이 복잡할 수 있으므로 상세 내용을 확인해 주세요.")
    else:
        score += 10

    if request.amount is not None and product.max_limit is not None:
        if request.amount <= product.max_limit:
            score += 10
            reason_tags.append("입력 금액 조건 적합")
        else:
            warnings.append("입력 금액이 상품 한도를 초과할 수 있습니다.")

    normalized_score = round(min(score, 100), 1)
    explanation = _build_explanation(product, request, reason_tags)
    return RecommendationResult(
        product=product,
        score=normalized_score,
        reason_tags=reason_tags,
        explanation=explanation,
        warnings=warnings,
    )


def _select_option(product: Product, term_months: int) -> ProductOption | None:
    return next((option for option in product.options if option.term_months == term_months), None)


def _build_explanation(
    product: Product,
    request: RecommendationRequest,
    reason_tags: list[str],
) -> str:
    reasons = ", ".join(reason_tags) if reason_tags else "입력 조건과 비교 가능한 항목"
    return (
        f"{product.product_name}은(는) {request.term_months}개월 기준으로 {reasons}을(를) "
        "확인할 수 있어 우선 비교할 상품으로 제안합니다."
    )
