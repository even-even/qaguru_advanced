import pytest

from tests.src import assert_helpers


@pytest.mark.usefixtures("server")
class TestsMyProject:
    """Тесты на написанный мной FastApi сервис"""
    def test_create_user(self, users_request):
        body = {"name": "john", "job": "qa"}

        response = users_request.create_user(body)
        response_body = response.json()
        assert response_body["id"] > 0

        assert_helpers.check_status_code(response, 201)

    def test_get_user_by_id(self, users_request):
        user_id = 12
        expected_email = "rachel.howell@reqres.in"
        expected_name = "Rachel"

        response = users_request.get_user_by_id(user_id)
        body = response.json()

        assert_helpers.check_status_code(response, 200)
        assert body["email"] == expected_email
        assert body["first_name"] == expected_name

    def test_update_user(self, users_request):
        user_id = 11
        new_data = {
            "name": "Hannah",
            "job": "Senior QA",
            "email": "hannah.smith@example.com"
        }
        response = users_request.put_user_by_id(user_id, json=new_data)
        assert_helpers.check_status_code(response, 200)
        updated_user = response.json()
        assert updated_user["name"] == "Hannah"
        assert updated_user["job"] == "Senior QA"
        assert updated_user["email"] == "hannah.smith@example.com"

    def test_delete_user(self, users_request):
        user_id = 2
        response = users_request.delete_user(user_id)

        assert_helpers.check_status_code(response, 204)
        assert_helpers.check_status_code(users_request.get_user_by_id(user_id), 404)

    def test_get_users_list(self, users_request):
        response = users_request.get_users_list()

        assert_helpers.check_status_code(response, 200)
