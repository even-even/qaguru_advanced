
import allure
import pytest

from app.models.user import User
from tests.src import assert_helpers


@pytest.mark.usefixtures("server", "fill_test_data")
class TestGetUsersList:

    @allure.title("Запрос списка пользователей")
    def test_get_users_list(self, users_request):
        response = users_request.get_users_list(None)

        assert_helpers.check_status_code(response, 200)

        users = response.json()
        for user in users:
            User.model_validate(user)

    @allure.title("В списке пользователей уникальные значения")
    def test_users_no_duplicates(self, users_list):

        users_ids = [user["id"] for user in users_list]
        assert len(users_ids) == len(set(users_ids)), f"Обнаружены дубликаты: {users_ids.remove(set(users_ids))}"
