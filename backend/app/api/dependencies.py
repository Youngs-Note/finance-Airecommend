from collections.abc import Iterator

from backend.app.core.config import get_settings
from backend.app.services.ai_explainer import AIExplainer
from backend.app.services.product_service import ProductService


def get_product_service() -> Iterator[ProductService]:
    yield ProductService(get_settings())


def get_ai_explainer() -> AIExplainer:
    return AIExplainer(get_settings())
