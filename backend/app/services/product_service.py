from collections.abc import Iterable

from backend.app.core.config import Settings
from backend.app.core.errors import ProductNotFoundError
from backend.app.data.sample_products import get_sample_products
from backend.app.schemas.product import Product, ProductType
from backend.app.services.finlife_client import FinlifeClient


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
        product_types = [product_type] if product_type else list(ProductType)
        client = FinlifeClient(self.settings)
        try:
            return [
                product
                for current_product_type in product_types
                for product in client.fetch_products(current_product_type)
            ]
        finally:
            client.close()


def _highest_rate_sort_key(product: Product) -> float:
    return product.highest_rate or -1
