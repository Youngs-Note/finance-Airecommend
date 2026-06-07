from typing import Any

import httpx

from backend.app.core.config import Settings
from backend.app.core.errors import ConfigurationError, ExternalApiError
from backend.app.schemas.product import Product, ProductType
from backend.app.services.product_normalizer import normalize_finlife_products

ENDPOINTS = {
    ProductType.DEPOSIT: "depositProductsSearch.json",
    ProductType.SAVING: "savingProductsSearch.json",
}


class FinlifeClient:
    def __init__(
        self,
        settings: Settings,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.settings = settings
        self.http_client = http_client or httpx.Client(timeout=settings.finlife_timeout_seconds)
        self._owns_http_client = http_client is None

    def close(self) -> None:
        if self._owns_http_client:
            self.http_client.close()

    def fetch_products(self, product_type: ProductType) -> list[Product]:
        self._validate_settings()
        payloads = self._fetch_all_pages(product_type)
        products: list[Product] = []
        for payload in payloads:
            products.extend(
                normalize_finlife_products(
                    payload=payload,
                    product_type=product_type,
                    allowed_banks=self.settings.allowed_banks,
                )
            )
        return products

    def _validate_settings(self) -> None:
        if not self.settings.finlife_api_key:
            raise ConfigurationError(
                "APP_DATA_MODE=finlife requires the FINLIFE_API_KEY environment variable."
            )
        if not self.settings.allowed_banks:
            raise ConfigurationError(
                "APP_DATA_MODE=finlife requires FINLIFE_ALLOWED_BANKS to prevent unintended "
                "bank exposure."
            )

    def _fetch_all_pages(self, product_type: ProductType) -> list[dict[str, Any]]:
        page_number = 1
        pages: list[dict[str, Any]] = []

        while True:
            payload = self._fetch_page(product_type, page_number)
            pages.append(payload)
            result = payload.get("result", {})
            max_page_number = int(result.get("max_page_no", page_number))
            if page_number >= max_page_number:
                return pages
            page_number += 1

    def _fetch_page(self, product_type: ProductType, page_number: int) -> dict[str, Any]:
        url = f"{self.settings.finlife_base_url.rstrip('/')}/{ENDPOINTS[product_type]}"
        params = {
            "auth": self.settings.finlife_api_key,
            "topFinGrpNo": self.settings.finlife_bank_group_code,
            "pageNo": page_number,
        }

        try:
            response = self.http_client.get(url, params=params)
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise ExternalApiError("Unable to load financial products from Finlife.") from exc

        result = payload.get("result", {})
        if result.get("err_cd") != "000":
            message = result.get("err_msg", "Unknown Finlife API error")
            raise ExternalApiError(f"Finlife API error: {message}")

        return payload
