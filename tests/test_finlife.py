from typing import Any

import httpx
import pytest

from backend.app.core.config import Settings
from backend.app.core.errors import ConfigurationError
from backend.app.schemas.product import ProductType
from backend.app.services.finlife_client import FinlifeClient
from backend.app.services.product_normalizer import normalize_finlife_products


def _payload(
    *,
    page_number: int = 1,
    max_page_number: int = 1,
    bank_name: str = "허용은행",
    product_code: str = "product-a",
) -> dict[str, Any]:
    return {
        "result": {
            "err_cd": "000",
            "err_msg": "success",
            "now_page_no": page_number,
            "max_page_no": max_page_number,
            "baseList": [
                {
                    "fin_co_no": "bank-a",
                    "fin_prdt_cd": product_code,
                    "kor_co_nm": bank_name,
                    "fin_prdt_nm": f"테스트 상품 {product_code}",
                    "join_way": "인터넷, 스마트폰",
                }
            ],
            "optionList": [
                {
                    "fin_co_no": "bank-a",
                    "fin_prdt_cd": product_code,
                    "save_trm": "12",
                    "intr_rate": 2.5,
                    "intr_rate2": 3.0,
                }
            ],
        }
    }


def test_normalizer_excludes_banks_outside_the_allowlist() -> None:
    products = normalize_finlife_products(
        payload=_payload(bank_name="제외은행"),
        product_type=ProductType.DEPOSIT,
        allowed_banks={"허용은행"},
    )

    assert products == []


def test_normalizer_returns_allowed_bank_product() -> None:
    products = normalize_finlife_products(
        payload=_payload(),
        product_type=ProductType.DEPOSIT,
        allowed_banks={"허용은행"},
    )

    assert len(products) == 1
    assert products[0].bank_name == "허용은행"
    assert products[0].highest_rate == 3.0


def test_normalizer_does_not_invent_values_for_malformed_option() -> None:
    payload = _payload()
    payload["result"]["optionList"][0]["save_trm"] = "unknown"
    payload["result"]["optionList"][0]["intr_rate"] = "unknown"

    products = normalize_finlife_products(
        payload=payload,
        product_type=ProductType.DEPOSIT,
        allowed_banks={"허용은행"},
    )

    assert len(products) == 1
    assert products[0].options == []


def test_finlife_client_requires_api_key_and_allowlist() -> None:
    client = FinlifeClient(Settings(app_data_mode="finlife", finlife_allowed_banks=""))

    with pytest.raises(ConfigurationError):
        client.fetch_products(ProductType.DEPOSIT)

    client.close()


def test_default_allowlist_matches_product_scope() -> None:
    allowed_banks = Settings().allowed_banks

    assert "국민은행" in allowed_banks
    assert "토스뱅크" in allowed_banks
    assert "주식회사 하나은행" in allowed_banks
    assert allowed_banks.isdisjoint(
        {
            "아이엠뱅크",
            "iM은행",
            "부산은행",
            "BNK부산은행",
            "광주은행",
            "제주은행",
            "전북은행",
            "경남은행",
            "BNK경남은행",
        }
    )
    assert "한국산업은행" not in allowed_banks
    assert "중소기업은행" not in allowed_banks
    assert "농협은행주식회사" not in allowed_banks
    assert "수협은행" not in allowed_banks


def test_finlife_client_fetches_all_pages() -> None:
    requested_pages: list[str] = []

    def handle_request(request: httpx.Request) -> httpx.Response:
        page_number = request.url.params["pageNo"]
        requested_pages.append(page_number)
        return httpx.Response(
            200,
            json=_payload(
                page_number=int(page_number),
                max_page_number=2,
                product_code=f"product-{page_number}",
            ),
        )

    http_client = httpx.Client(transport=httpx.MockTransport(handle_request))
    client = FinlifeClient(
        Settings(
            app_data_mode="finlife",
            finlife_api_key="test-key",
            finlife_allowed_banks="허용은행",
        ),
        http_client=http_client,
    )

    products = client.fetch_products(ProductType.DEPOSIT)

    assert requested_pages == ["1", "2"]
    assert len(products) == 2
    http_client.close()
