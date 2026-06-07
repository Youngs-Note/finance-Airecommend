from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field, HttpUrl


class ProductType(StrEnum):
    DEPOSIT = "deposit"
    SAVING = "saving"


class DataSource(StrEnum):
    FINLIFE = "finlife"
    SAMPLE = "sample"


class ProductOption(BaseModel):
    term_months: int = Field(ge=1)
    base_rate: float | None = Field(default=None, ge=0)
    max_rate: float | None = Field(default=None, ge=0)
    interest_type: str | None = None
    saving_type: str | None = None


class Product(BaseModel):
    id: str
    source: DataSource
    source_company_code: str
    source_product_code: str
    product_type: ProductType
    bank_name: str
    product_name: str
    join_way: list[str] = Field(default_factory=list)
    join_member: str | None = None
    special_conditions: str | None = None
    maturity_interest: str | None = None
    notes: str | None = None
    max_limit: int | None = Field(default=None, ge=0)
    disclosure_month: str | None = None
    disclosed_at: str | None = None
    collected_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source_url: HttpUrl
    options: list[ProductOption] = Field(default_factory=list)

    @property
    def highest_rate(self) -> float | None:
        rates = [
            rate
            for option in self.options
            for rate in [option.max_rate, option.base_rate]
            if rate is not None
        ]
        return max(rates, default=None)
