from backend.app.core.config import Settings
from backend.app.core.errors import ExternalApiError
from backend.app.schemas.product import DataSource, Product, ProductOption, ProductType
from backend.app.services import product_service as product_service_module
from backend.app.services.product_service import ProductService


def _cached_product() -> Product:
    return Product(
        id="finlife:deposit:bank-a:deposit-a",
        source=DataSource.FINLIFE,
        source_company_code="bank-a",
        source_product_code="deposit-a",
        product_type=ProductType.DEPOSIT,
        bank_name="국민은행",
        product_name="캐시 정기예금",
        source_url="https://finlife.fss.or.kr/",
        options=[ProductOption(term_months=12, base_rate=3.1, max_rate=3.5)],
    )


def test_finlife_mode_falls_back_to_cached_products(monkeypatch) -> None:
    def raise_external_api_error(_client, _product_type):
        raise ExternalApiError("Finlife unavailable")

    monkeypatch.setattr(
        product_service_module.FinlifeClient,
        "fetch_products",
        raise_external_api_error,
    )
    monkeypatch.setattr(
        product_service_module,
        "load_finlife_cached_products",
        lambda product_type=None: [_cached_product()],
    )

    service = ProductService(Settings(app_data_mode="finlife", finlife_api_key="test-key"))

    products = service.list_products(product_type=ProductType.DEPOSIT)

    assert len(products) == 1
    assert products[0].source == DataSource.FINLIFE
    assert products[0].product_name == "캐시 정기예금"


def test_finlife_mode_raises_when_live_api_and_cache_are_unavailable(monkeypatch) -> None:
    def raise_external_api_error(_client, _product_type):
        raise ExternalApiError("Finlife unavailable")

    monkeypatch.setattr(
        product_service_module.FinlifeClient,
        "fetch_products",
        raise_external_api_error,
    )
    monkeypatch.setattr(
        product_service_module,
        "load_finlife_cached_products",
        lambda product_type=None: [],
    )

    service = ProductService(Settings(app_data_mode="finlife", finlife_api_key="test-key"))

    try:
        service.list_products(product_type=ProductType.DEPOSIT)
    except ExternalApiError:
        return

    raise AssertionError("Expected ExternalApiError when cache is unavailable.")
