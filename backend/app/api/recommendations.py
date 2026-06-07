from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.api.dependencies import get_ai_explainer, get_product_service
from backend.app.schemas.recommendation import RecommendationRequest, RecommendationResult
from backend.app.services.ai_explainer import AIExplainer
from backend.app.services.product_service import ProductService
from backend.app.services.recommender import recommend_products

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])
ProductServiceDependency = Annotated[ProductService, Depends(get_product_service)]
AIExplainerDependency = Annotated[AIExplainer, Depends(get_ai_explainer)]


@router.post("", response_model=list[RecommendationResult])
def recommend(
    request: RecommendationRequest,
    service: ProductServiceDependency,
    explainer: AIExplainerDependency,
) -> list[RecommendationResult]:
    products = service.list_products(product_type=request.product_type)
    results = recommend_products(products, request)
    return explainer.enhance_recommendations(results, request)
