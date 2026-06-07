from collections import defaultdict
from datetime import UTC, datetime
from typing import Any

from backend.app.schemas.product import DataSource, Product, ProductOption, ProductType

FINLIFE_SOURCE_URL = "https://finlife.fss.or.kr/"


def normalize_finlife_products(
    payload: dict[str, Any],
    product_type: ProductType,
    allowed_banks: set[str],
) -> list[Product]:
    """Normalize a Finlife response without storing the original payload."""

    result = payload.get("result", payload)
    option_groups: dict[tuple[str, str], list[ProductOption]] = defaultdict(list)

    for option in result.get("optionList", []):
        term_months = _to_int(option.get("save_trm"))
        if term_months is None or term_months < 1:
            continue
        key = (str(option.get("fin_co_no", "")), str(option.get("fin_prdt_cd", "")))
        option_groups[key].append(
            ProductOption(
                term_months=term_months,
                base_rate=_to_float(option.get("intr_rate")),
                max_rate=_to_float(option.get("intr_rate2")),
                interest_type=_clean_text(option.get("intr_rate_type_nm")),
                saving_type=_clean_text(option.get("rsrv_type_nm")),
            )
        )

    products: list[Product] = []
    collected_at = datetime.now(UTC)

    for product in result.get("baseList", []):
        bank_name = _clean_text(product.get("kor_co_nm")) or ""
        if bank_name not in allowed_banks:
            continue

        company_code = str(product.get("fin_co_no", ""))
        product_code = str(product.get("fin_prdt_cd", ""))
        key = (company_code, product_code)
        products.append(
            Product(
                id=f"finlife:{product_type.value}:{company_code}:{product_code}",
                source=DataSource.FINLIFE,
                source_company_code=company_code,
                source_product_code=product_code,
                product_type=product_type,
                bank_name=bank_name,
                product_name=_clean_text(product.get("fin_prdt_nm")) or "",
                join_way=_split_join_way(product.get("join_way")),
                join_member=_clean_text(product.get("join_member")),
                special_conditions=_clean_text(product.get("spcl_cnd")),
                maturity_interest=_clean_text(product.get("mtrt_int")),
                notes=_clean_text(product.get("etc_note")),
                max_limit=_to_int(product.get("max_limit")),
                disclosure_month=_clean_text(product.get("dcls_month")),
                disclosed_at=_clean_text(product.get("fin_co_subm_day")),
                collected_at=collected_at,
                source_url=FINLIFE_SOURCE_URL,
                options=option_groups[key],
            )
        )

    return products


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _split_join_way(value: Any) -> list[str]:
    text = _clean_text(value)
    if text is None:
        return []
    return [item.strip() for item in text.split(",") if item.strip()]


def _to_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None
