import pytest

from tests.src.api_client.app_status import AppStatusRequest
from tests.src.api_client.users import UsersRequest
from tests.src.config.settings import AppSettings


def pytest_addoption(parser):
    """Добавляем кастомные опции командной строки."""
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        choices=["dev", "stage", "prod"],
        help="Окружение для тестов: dev, stage, prod"
    )


@pytest.fixture(scope="session")
def app_settings(pytestconfig):
    """Фикстура для настроек приложения."""
    env = pytestconfig.getoption("--env")
    return AppSettings(env=env)


@pytest.fixture(scope="session")
def users_request(app_settings) -> UsersRequest:
    """Фикстура для клиента Users API."""
    return UsersRequest(env=app_settings.env)


@pytest.fixture(scope="session")
def app_status_request(app_settings) -> AppStatusRequest:
    """Фикстура для клиента Users API."""
    return AppStatusRequest(env=app_settings.env)
