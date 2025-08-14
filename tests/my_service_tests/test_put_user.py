import allure
import pytest

from tests.src import assert_helpers


@pytest.mark.usefixtures("server")
class TestsPutUser:

    @allure.title("Редактирование пользователя")
    def test_update_user(self, users_request):
        user_id = 7
        new_data = {
            "name": "Hannah",
            "email": "hannah.smith@example.com"
        }
        response = users_request.put_user_by_id(user_id, json=new_data)
        assert_helpers.check_status_code(response, 200)
        updated_user = response.json()
        assert updated_user["name"] == "Hannah"
        assert updated_user["email"] == "hannah.smith@example.com"
