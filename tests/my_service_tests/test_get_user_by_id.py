import allure
import pytest

from tests.src import assert_helpers


@pytest.mark.usefixtures("server", "fill_test_data")
class TestGetUserById:

    @allure.title("Запрос пользователя по id")
    def test_get_user_by_id(self, users_request):
        user_id = 12
        expected_email = "rachel.howell@reqres.in"
        expected_name = "Rachel"
        response = users_request.get_user_by_id(user_id)
        body = response.json()

        assert_helpers.check_status_code(response, 200)
        assert body["email"] == expected_email
        assert body["first_name"] == expected_name


@pytest.mark.usefixtures("server", "fill_test_data")
class TestGetUserByIdNegative:

    @allure.title("Запрос несуществующего пользователя невозможен")
    def test_user_non_exist_404(self, users_request):
        response = users_request.get_user_by_id(99999)
        assert_helpers.check_status_code(response, 404)

    @pytest.mark.parametrize("user_id", [-1, 0, "string", None])
    def test_user_invalid_id_422(self, users_request, user_id):
        allure.dynamic.title(f"Запрос пользователя с некорректным user_id={user_id} невозможен")

        response = users_request.get_user_by_id(user_id)
        assert_helpers.check_status_code(response, 422)
