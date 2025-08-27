import allure
import pytest

from tests.src import assert_helpers
from tests.src.data_generators import get_random_string


@pytest.mark.usefixtures("fill_test_data")
class TestsPatchUser:

    @allure.title("Редактирование пользователя")
    def test_patch_user(self, create_user, users_request):
        user_id = create_user["id"]
        email_after = "email_after@example.com"
        first_name_after = "first_name_after"
        last_name_after = "last_name_after"
        avatar_after = "http://avatar.autotest.ru/avatar_after"

        new_data = {"email": email_after,
            "first_name": first_name_after,
            "last_name": last_name_after,
            "avatar": avatar_after}

        response = users_request.patch_user(user_id, json=new_data)
        assert_helpers.check_status_code(response, 200)
        updated_user = response.json()
        assert updated_user["email"] == email_after
        assert updated_user["first_name"] == first_name_after
        assert updated_user["last_name"] == last_name_after
        assert updated_user["avatar"] == avatar_after


@pytest.mark.usefixtures("fill_test_data")
class TestsPatchUserNegative:

    @allure.title("Редактирование несуществующего пользователя невозможно")
    def test_patch_user_not_exist_id_404(self, users_request):
        response = users_request.patch_user(user_id=9999999999, json={
            "first_name": f"autotest_patch_name_{get_random_string()}"})

        assert_helpers.check_status_code(response, 404)
