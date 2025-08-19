import allure
import pytest

from tests.src import assert_helpers
from tests.src.api_client.app_status import AppStatusRequest


@pytest.mark.usefixtures("server")
class TestsAppStatus:

    @allure.title("Проверка доступности микросервиса")
    def test_status(self):
        response = AppStatusRequest().get_status()
        assert_helpers.check_status_code(response, 200)
