import pymysql

from backend.app.core.config import Settings
from backend.app.services.mysql_health import check_mysql_connection


class FakeCursor:
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def execute(self, query: str) -> None:
        assert query == "SELECT 1"


class FakeConnection:
    closed = False

    def cursor(self) -> FakeCursor:
        return FakeCursor()

    def close(self) -> None:
        self.closed = True


def test_mysql_health_check_is_disabled_by_default() -> None:
    status = check_mysql_connection(Settings(mysql_enabled=False))

    assert status.enabled is False
    assert status.connected is False


def test_mysql_health_check_reports_available_connection() -> None:
    connection = FakeConnection()

    status = check_mysql_connection(
        Settings(mysql_enabled=True),
        connect=lambda **_kwargs: connection,
    )

    assert status.connected is True
    assert connection.closed is True


def test_mysql_health_check_hides_connection_error_details() -> None:
    def raise_error(**_kwargs):
        raise pymysql.MySQLError("do not expose credentials or host details")

    status = check_mysql_connection(
        Settings(mysql_enabled=True),
        connect=raise_error,
    )

    assert status.connected is False
    assert status.detail == "MySQL connection is unavailable."
