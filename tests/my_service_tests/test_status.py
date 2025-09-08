import allure
import pytest

from tests.src import assert_helpers


@pytest.mark.usefixtures("fill_test_data")
class TestsAppStatus:

    @allure.title("Проверка доступности микросервиса")
    def test_status(self, app_status_request):
        response = app_status_request.get_status()
        assert_helpers.check_status_code(response, 200)
