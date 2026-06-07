from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from backend.app.api.dependencies import get_ai_explainer, get_product_service
from backend.app.schemas.ai import ComparisonSummary
from backend.app.schemas.product import Product, ProductType
from backend.app.services.ai_explainer import AIExplainer
from backend.app.services.product_service import ProductService

router = APIRouter(prefix="/api/products", tags=["products"])
ProductServiceDependency = Annotated[ProductService, Depends(get_product_service)]
AIExplainerDependency = Annotated[AIExplainer, Depends(get_ai_explainer)]


class CompareProductsRequest(BaseModel):
    product_ids: list[str] = Field(min_length=2, max_length=3)


@router.get("", response_model=list[Product])
def list_products(
    service: ProductServiceDependency,
    product_type: ProductType | None = None,
    bank_name: str | None = None,
    term_months: int | None = Query(default=None, ge=1, le=120),
) -> list[Product]:
    return service.list_products(
        product_type=product_type,
        bank_name=bank_name,
        term_months=term_months,
    )


@router.post("/compare", response_model=list[Product])
def compare_products(
    request: CompareProductsRequest,
    service: ProductServiceDependency,
) -> list[Product]:
    return service.compare_products(request.product_ids)


@router.post("/compare-summary", response_model=ComparisonSummary)
def summarize_comparison(
    request: CompareProductsRequest,
    service: ProductServiceDependency,
    explainer: AIExplainerDependency,
) -> ComparisonSummary:
    products = service.compare_products(request.product_ids)
    return explainer.summarize_comparison(products)


@router.get("/{product_id}", response_model=Product)
def get_product(
    product_id: str,
    service: ProductServiceDependency,
) -> Product:
    return service.get_product(product_id)
