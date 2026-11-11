from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.app.core.banks import DEFAULT_ALLOWED_BANKS


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "finance-Airecommend API"
    app_env: str = "development"
    app_data_mode: Literal["sample", "finlife"] = "sample"

    finlife_api_key: str | None = None
    finlife_base_url: str = "https://finlife.fss.or.kr/finlifeapi"
    finlife_bank_group_code: str = "020000"
    finlife_allowed_banks: str = ",".join(DEFAULT_ALLOWED_BANKS)
    finlife_timeout_seconds: float = Field(default=10.0, gt=0)
    finlife_cache_ttl_seconds: float = Field(default=21_600.0, ge=0)

    openai_explanations_enabled: bool = False
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.4-mini"
    openai_timeout_seconds: float = Field(default=15.0, gt=0)

    mysql_enabled: bool = False
    mysql_host: str = "localhost"
    mysql_port: int = Field(default=3306, ge=1, le=65535)
    mysql_database: str = "finance_ai"
    mysql_user: str = "finance_ai"
    mysql_password: str | None = None

    @property
    def allowed_banks(self) -> set[str]:
        return {
            bank_name.strip()
            for bank_name in self.finlife_allowed_banks.split(",")
            if bank_name.strip()
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
