from collections import defaultdict
from statistics import mean
from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.api.dependencies import get_product_service
from backend.app.schemas.product import ProductType
from backend.app.services.product_service import ProductService

router = APIRouter(prefix="/api/stats", tags=["stats"])
ProductServiceDependency = Annotated[ProductService, Depends(get_product_service)]


@router.get("/rates")
def rate_stats(
    service: ProductServiceDependency,
    product_type: ProductType | None = None,
) -> list[dict[str, int | float | str]]:
    products = service.list_products(product_type=product_type)
    grouped: dict[ProductType, list[float]] = defaultdict(list)
    for product in products:
        if product.highest_rate is not None:
            grouped[product.product_type].append(product.highest_rate)

    return [
        {
            "product_type": current_type,
            "product_count": len(rates),
            "average_highest_rate": round(mean(rates), 3),
            "maximum_rate": max(rates),
            "minimum_rate": min(rates),
        }
        for current_type, rates in sorted(grouped.items())
    ]
