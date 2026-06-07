from collections.abc import Iterable
from dataclasses import dataclass, field
from time import monotonic

from backend.app.core.config import Settings
from backend.app.core.errors import ExternalApiError, ProductNotFoundError
from backend.app.data.finlife_cache import load_finlife_cached_products
from backend.app.data.sample_products import get_sample_products
from backend.app.schemas.product import Product, ProductType
from backend.app.services.finlife_client import FinlifeClient


@dataclass
class FinlifeProductsCache:
    fetched_at: float = 0.0
    products_by_type: dict[ProductType, list[Product]] = field(default_factory=dict)

    def is_fresh(self, ttl_seconds: float, now: float) -> bool:
        return (
            bool(self.products_by_type) and ttl_seconds > 0 and now - self.fetched_at < ttl_seconds
        )


_finlife_products_cache = FinlifeProductsCache()


class ProductService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def list_products(
        self,
        product_type: ProductType | None = None,
        bank_name: str | None = None,
        term_months: int | None = None,
    ) -> list[Product]:
        products = self._load_products(product_type)
        if bank_name:
            products = [product for product in products if product.bank_name == bank_name]
        if term_months:
            products = [
                product
                for product in products
                if any(option.term_months == term_months for option in product.options)
            ]
        return sorted(products, key=_highest_rate_sort_key, reverse=True)

    def get_product(self, product_id: str) -> Product:
        for product in self._load_products():
            if product.id == product_id:
                return product
        raise ProductNotFoundError(f"Product not found: {product_id}")

    def compare_products(self, product_ids: Iterable[str]) -> list[Product]:
        return [self.get_product(product_id) for product_id in product_ids]

    def _load_products(self, product_type: ProductType | None = None) -> list[Product]:
        if self.settings.app_data_mode == "sample":
            products = get_sample_products()
        else:
            products = self._load_finlife_products(product_type)

        if product_type is None:
            return products
        return [product for product in products if product.product_type == product_type]

    def _load_finlife_products(self, product_type: ProductType | None) -> list[Product]:
        now = monotonic()
        if _finlife_products_cache.is_fresh(self.settings.finlife_cache_ttl_seconds, now):
            return _select_products_from_cache(product_type)

        product_types = list(ProductType)
        client = FinlifeClient(self.settings)
        try:
            products_by_type = {
                current_product_type: client.fetch_products(current_product_type)
                for current_product_type in product_types
            }
            _store_products_by_type_in_cache(products_by_type, now)
            return _select_products_from_cache(product_type)
        except ExternalApiError:
            stale_products = _select_products_from_cache(product_type)
            if stale_products:
                return stale_products
            cached_products = load_finlife_cached_products()
            if cached_products:
                _store_products_in_cache(cached_products, now)
                return _select_products_from_cache(product_type)
            raise
        finally:
            client.close()


def _highest_rate_sort_key(product: Product) -> float:
    return product.highest_rate or -1


def _select_products_from_cache(product_type: ProductType | None) -> list[Product]:
    if product_type is not None:
        return list(_finlife_products_cache.products_by_type.get(product_type, []))
    return [
        product
        for products in _finlife_products_cache.products_by_type.values()
        for product in products
    ]


def _store_products_by_type_in_cache(
    products_by_type: dict[ProductType, list[Product]],
    fetched_at: float,
) -> None:
    _finlife_products_cache.products_by_type = {
        product_type: list(products) for product_type, products in products_by_type.items()
    }
    _finlife_products_cache.fetched_at = fetched_at


def _store_products_in_cache(products: list[Product], fetched_at: float) -> None:
    products_by_type = {
        product_type: [product for product in products if product.product_type == product_type]
        for product_type in ProductType
    }
    _store_products_by_type_in_cache(products_by_type, fetched_at)
