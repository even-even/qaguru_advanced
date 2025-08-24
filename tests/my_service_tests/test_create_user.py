import allure
import pytest

from app.models.user import UserCreate
from tests.src import assert_helpers
from tests.src.allure_decorators import After
from tests.src.data_generators import get_random_string


@pytest.mark.usefixtures("server", "fill_test_data")
class TestCreateUser:

    @allure.title("Создание пользователя")
    def test_create_user(self, users_request):

        email = f"{get_random_string().lower()}@autotest.ru"
        first_name = f"first_name_{get_random_string()}"
        last_name = f"last_name{get_random_string()}"
        avatar = f"http://avatar_autotest.ru/{get_random_string().lower()}"
        user = UserCreate(
            email=email,
            first_name=first_name,
            last_name=last_name,
            avatar=avatar
        ).model_dump()
        response = users_request.create_user(json=user)

        assert_helpers.check_status_code(response, 201)
        user_response = response.json()
        user_id = user_response["id"]

        try:
            assert_helpers.check_status_code(users_request.get_user_by_id(user_id), 200)
            assert user_response["email"] == email
            assert user_response["first_name"] == first_name
            assert user_response["last_name"] == last_name
            assert user_response["avatar"] == avatar

        finally:
            with After(f"Удалить пользователя {user_id} после окончания теста"):
                users_request.delete_user(user_id)
