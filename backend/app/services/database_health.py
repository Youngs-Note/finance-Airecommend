from collections.abc import Callable
from typing import Any

import psycopg

from backend.app.core.config import Settings
from backend.app.schemas.database import DatabaseStatus


def check_database_connection(
    settings: Settings,
    connect: Callable[..., Any] = psycopg.connect,
) -> DatabaseStatus:
    if not settings.database_enabled:
        return DatabaseStatus(
            enabled=False,
            connected=False,
            detail="Database connection check is disabled.",
        )

    if not settings.database_url:
        return DatabaseStatus(
            enabled=True,
            connected=False,
            detail="DATABASE_URL is not configured.",
        )

    # 접속 정보(호스트, 비밀번호)가 응답에 노출되지 않도록 오류 내용은 숨긴다.
    try:
        with connect(settings.database_url, connect_timeout=5) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        return DatabaseStatus(
            enabled=True,
            connected=True,
            detail="Database connection is available.",
        )
    except psycopg.Error:
        return DatabaseStatus(
            enabled=True,
            connected=False,
            detail="Database connection is unavailable.",
        )
