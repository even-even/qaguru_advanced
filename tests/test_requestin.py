from tests.src import assert_helpers


class TestsRequestIn:
    """Тесты на https://reqres.in"""

    # Все id захардкоженные т.к. по факту ничего не создается post запросом
    def test_create_user(self, users_request):
        payload = {"name": "John Doe", "job": "Developer"}
        response = users_request.create_user(payload, url="https://reqres.in")
        assert_helpers.check_status_code(response, 201)
        response_json = response.json()
        assert int(response_json["id"]) > 0
        assert response_json["job"] == "Developer"
        assert response_json["name"] == "John Doe"

    def test_get_user_by_id(self, users_request):
        user_id = 12
        response = users_request.get_user_by_id(user_id, url="https://reqres.in")
        assert_helpers.check_status_code(response, 200)
        assert response.json()["data"]["id"] == user_id

    def test_update_user(self, users_request):
        user_id = 11
        payload = {"name": "Jane Smith", "job": "Quality Assurance"}
        response = users_request.put_user_by_id(user_id, payload, url="https://reqres.in")
        assert_helpers.check_status_code(response, 200)
        assert response.json()["name"] == "Jane Smith"
        assert response.json()["job"] == "Quality Assurance"

    def test_delete_user(self, users_request):
        user_id = 1
        response = users_request.delete_user(user_id, url="https://reqres.in")
        assert_helpers.check_status_code(response, 204)

    def test_list_users(self, users_request):
        response = users_request.get_users_list(url="https://reqres.in")
        assert_helpers.check_status_code(response, 200)
        users = response.json()
        assert len(users) > 0
