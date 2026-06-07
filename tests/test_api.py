from fastapi.testclient import TestClient

from backend.app.api.dependencies import get_ai_explainer, get_product_service
from backend.app.core.config import Settings, get_settings
from backend.app.main import app
from backend.app.services.ai_explainer import AIExplainer
from backend.app.services.product_service import ProductService

sample_settings = Settings(
    _env_file=None,
    app_data_mode="sample",
    openai_explanations_enabled=False,
    openai_api_key=None,
    mysql_enabled=False,
)
app.dependency_overrides[get_settings] = lambda: sample_settings
app.dependency_overrides[get_product_service] = lambda: ProductService(sample_settings)
app.dependency_overrides[get_ai_explainer] = lambda: AIExplainer(sample_settings)
client = TestClient(app)


def test_health_reports_sample_mode() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["data_mode"] == "sample"


def test_list_products_can_filter_by_type_and_term() -> None:
    response = client.get("/api/products", params={"product_type": "deposit", "term_months": 12})

    assert response.status_code == 200
    products = response.json()
    assert len(products) == 2
    assert all(product["product_type"] == "deposit" for product in products)


def test_compare_products_returns_selected_products() -> None:
    response = client.post(
        "/api/products/compare",
        json={
            "product_ids": [
                "sample:deposit:sample-bank-a:deposit-a",
                "sample:deposit:sample-bank-b:deposit-b",
            ]
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_compare_summary_uses_fallback_without_openai_key() -> None:
    response = client.post(
        "/api/products/compare-summary",
        json={
            "product_ids": [
                "sample:deposit:sample-bank-a:deposit-a",
                "sample:deposit:sample-bank-b:deposit-b",
            ]
        },
    )

    assert response.status_code == 200
    assert response.json()["ai_generated"] is False


def test_recommendations_return_ranked_products() -> None:
    response = client.post(
        "/api/recommendations",
        json={"product_type": "saving", "term_months": 12, "max_results": 2},
    )

    assert response.status_code == 200
    recommendations = response.json()
    assert len(recommendations) == 2
    assert recommendations[0]["score"] >= recommendations[1]["score"]
    assert recommendations[0]["explanation"]


def test_rate_stats_cover_both_product_types() -> None:
    response = client.get("/api/stats/rates")

    assert response.status_code == 200
    assert {item["product_type"] for item in response.json()} == {"deposit", "saving"}


def test_unknown_product_returns_not_found() -> None:
    response = client.get("/api/products/unknown")

    assert response.status_code == 404
    assert "Product not found" in response.json()["detail"]


def test_root_reports_api_entrypoint() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"
