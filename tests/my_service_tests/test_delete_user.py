import allure
import pytest

from tests.src import assert_helpers


@pytest.mark.usefixtures("server", "fill_test_data")
class TestDeleteUsers:

    @allure.title("Удаление пользователя")
    def test_deactivate_user(self, create_user, users_request):
        user_id = create_user["id"]

        response = users_request.delete_user(user_id)
        assert_helpers.check_status_code(response, 200)


@pytest.mark.usefixtures("server", "fill_test_data")
class TestDeleteUsersNegative:

    @allure.title("Удаление несуществующего пользователя невозможно")
    def test_deactivate_user_not_exist_404(self, users_request):
        not_exist_user_id = 999999999
        response = users_request.delete_user(not_exist_user_id)
        assert_helpers.check_status_code(response, 404)
