from pydantic import BaseModel, Field

from backend.app.schemas.product import Product, ProductType


class RecommendationRequest(BaseModel):
    product_type: ProductType
    term_months: int = Field(ge=1, le=120)
    amount: int | None = Field(default=None, ge=0)
    prefer_simple_conditions: bool = False
    max_results: int = Field(default=5, ge=1, le=10)


class RecommendationResult(BaseModel):
    product: Product
    score: float = Field(ge=0, le=100)
    reason_tags: list[str]
    explanation: str
    warnings: list[str]
