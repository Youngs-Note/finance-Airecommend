import psycopg

from backend.app.core.config import Settings
from backend.app.services.database_health import check_database_connection

DATABASE_URL = "postgresql://user:secret@example.neon.tech/finance_ai?sslmode=require"


class FakeCursor:
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def execute(self, query: str) -> None:
        assert query == "SELECT 1"


class FakeConnection:
    closed = False

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.closed = True

    def cursor(self) -> FakeCursor:
        return FakeCursor()


def test_database_health_check_is_disabled_by_default() -> None:
    status = check_database_connection(Settings(_env_file=None, database_enabled=False))

    assert status.enabled is False
    assert status.connected is False


def test_database_health_check_requires_database_url() -> None:
    status = check_database_connection(
        Settings(_env_file=None, database_enabled=True, database_url=None)
    )

    assert status.connected is False
    assert status.detail == "DATABASE_URL is not configured."


def test_database_health_check_reports_available_connection() -> None:
    connection = FakeConnection()
    received: dict[str, object] = {}

    def connect(url: str, **kwargs):
        received["url"] = url
        received.update(kwargs)
        return connection

    status = check_database_connection(
        Settings(_env_file=None, database_enabled=True, database_url=DATABASE_URL),
        connect=connect,
    )

    assert status.connected is True
    assert connection.closed is True
    assert received["url"] == DATABASE_URL


def test_database_health_check_hides_connection_error_details() -> None:
    def raise_error(*_args, **_kwargs):
        raise psycopg.OperationalError("do not expose credentials or host details")

    status = check_database_connection(
        Settings(_env_file=None, database_enabled=True, database_url=DATABASE_URL),
        connect=raise_error,
    )

    assert status.connected is False
    assert status.detail == "Database connection is unavailable."
