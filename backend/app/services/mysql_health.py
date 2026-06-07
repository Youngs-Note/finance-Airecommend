from collections.abc import Callable
from typing import Any

import pymysql

from backend.app.core.config import Settings
from backend.app.schemas.database import MySQLStatus


def check_mysql_connection(
    settings: Settings,
    connect: Callable[..., Any] = pymysql.connect,
) -> MySQLStatus:
    if not settings.mysql_enabled:
        return MySQLStatus(
            enabled=False,
            connected=False,
            detail="MySQL connection check is disabled.",
        )

    connection = None
    try:
        connection = connect(
            host=settings.mysql_host,
            port=settings.mysql_port,
            user=settings.mysql_user,
            password=settings.mysql_password or "",
            database=settings.mysql_database,
            connect_timeout=3,
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return MySQLStatus(
            enabled=True,
            connected=True,
            detail="MySQL connection is available.",
        )
    except pymysql.MySQLError:
        return MySQLStatus(
            enabled=True,
            connected=False,
            detail="MySQL connection is unavailable.",
        )
    finally:
        if connection is not None:
            connection.close()
