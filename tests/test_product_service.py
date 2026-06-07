from backend.app.core.config import Settings
from backend.app.core.errors import ExternalApiError
from backend.app.schemas.product import DataSource, Product, ProductOption, ProductType
from backend.app.services import product_service as product_service_module
from backend.app.services.product_service import ProductService


def setup_function() -> None:
    product_service_module._finlife_products_cache.fetched_at = 0.0
    product_service_module._finlife_products_cache.products_by_type = {}


def _cached_product(
    product_type: ProductType = ProductType.DEPOSIT,
    product_code: str = "deposit-a",
    product_name: str = "캐시 정기예금",
) -> Product:
    return Product(
        id=f"finlife:{product_type.value}:bank-a:{product_code}",
        source=DataSource.FINLIFE,
        source_company_code="bank-a",
        source_product_code=product_code,
        product_type=product_type,
        bank_name="국민은행",
        product_name=product_name,
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


def test_finlife_mode_reuses_memory_cache_within_ttl(monkeypatch) -> None:
    fetch_counts = {ProductType.DEPOSIT: 0, ProductType.SAVING: 0}

    def fetch_products(_client, product_type):
        fetch_counts[product_type] += 1
        return [_cached_product(product_type=product_type, product_code=f"{product_type.value}-a")]

    monkeypatch.setattr(
        product_service_module.FinlifeClient,
        "fetch_products",
        fetch_products,
    )
    monkeypatch.setattr(product_service_module, "monotonic", lambda: 100.0)

    service = ProductService(
        Settings(
            app_data_mode="finlife",
            finlife_api_key="test-key",
            finlife_cache_ttl_seconds=60,
        )
    )

    first_products = service.list_products(product_type=ProductType.DEPOSIT)
    second_products = service.list_products(product_type=ProductType.DEPOSIT)
    saving_products = service.list_products(product_type=ProductType.SAVING)

    assert first_products == second_products
    assert saving_products[0].product_type == ProductType.SAVING
    assert fetch_counts == {ProductType.DEPOSIT: 1, ProductType.SAVING: 1}


def test_finlife_mode_refreshes_memory_cache_after_ttl(monkeypatch) -> None:
    now = 100.0
    fetch_count = 0

    def current_time():
        return now

    def fetch_products(_client, product_type):
        nonlocal fetch_count
        fetch_count += 1
        return [
            _cached_product(
                product_type=product_type,
                product_code=f"{product_type.value}-{fetch_count}",
                product_name=f"캐시 상품 {fetch_count}",
            )
        ]

    monkeypatch.setattr(
        product_service_module.FinlifeClient,
        "fetch_products",
        fetch_products,
    )
    monkeypatch.setattr(product_service_module, "monotonic", current_time)

    service = ProductService(
        Settings(
            app_data_mode="finlife",
            finlife_api_key="test-key",
            finlife_cache_ttl_seconds=10,
        )
    )

    first_products = service.list_products(product_type=ProductType.DEPOSIT)
    now = 111.0
    refreshed_products = service.list_products(product_type=ProductType.DEPOSIT)

    assert first_products[0].id != refreshed_products[0].id
    assert fetch_count == 4


def test_finlife_mode_uses_stale_memory_cache_when_refresh_fails(monkeypatch) -> None:
    now = 100.0
    fetch_count = 0

    def current_time():
        return now

    def fetch_products(_client, product_type):
        nonlocal fetch_count
        fetch_count += 1
        if fetch_count > 2:
            raise ExternalApiError("Finlife unavailable")
        return [
            _cached_product(
                product_type=product_type,
                product_code=f"{product_type.value}-live",
                product_name="마지막 성공 상품",
            )
        ]

    monkeypatch.setattr(
        product_service_module.FinlifeClient,
        "fetch_products",
        fetch_products,
    )
    monkeypatch.setattr(product_service_module, "monotonic", current_time)
    monkeypatch.setattr(
        product_service_module,
        "load_finlife_cached_products",
        lambda product_type=None: [],
    )

    service = ProductService(
        Settings(
            app_data_mode="finlife",
            finlife_api_key="test-key",
            finlife_cache_ttl_seconds=10,
        )
    )

    service.list_products(product_type=ProductType.DEPOSIT)
    now = 111.0
    stale_products = service.list_products(product_type=ProductType.DEPOSIT)

    assert stale_products[0].product_name == "마지막 성공 상품"
    assert fetch_count == 3


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
