import json
from pathlib import Path

from backend.app.schemas.product import Product, ProductType

FINLIFE_CACHE_PATH = Path(__file__).with_name("finlife_products.json")


def load_finlife_cached_products(product_type: ProductType | None = None) -> list[Product]:
    if not FINLIFE_CACHE_PATH.exists():
        return []

    raw_products = json.loads(FINLIFE_CACHE_PATH.read_text(encoding="utf-8"))
    products = [Product.model_validate(product) for product in raw_products]
    if product_type is None:
        return products
    return [product for product in products if product.product_type == product_type]
