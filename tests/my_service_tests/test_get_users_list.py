from math import ceil

import allure
import pytest

from app.models.user import User
from tests.src import assert_helpers


@pytest.fixture
def all_users(users_request):
    response = users_request.get_users_list()
    assert_helpers.check_status_code(response, 200)
    return response.json()


@pytest.mark.usefixtures("server")
class TestGetUsersList:

    @allure.title("Запрос списка пользователей")
    def test_get_users_list(self, users_request):
        response = users_request.get_users_list(None)

        assert_helpers.check_status_code(response, 200)

        users = response.json()
        for user in users["items"]:
            User.model_validate(user)

    @allure.title("В списке пользователей уникальные значения")
    def test_users_no_duplicates(self, users_list):
        users_ids = [user["id"] for user in users_list["items"]]
        assert len(users_ids) == len(set(users_ids)), f"Обнаружены дубликаты: {users_ids.remove(set(users_ids))}"

    @pytest.mark.parametrize(
        "page, size",
        [(1, 1), (12, 1), (1, 3), (2, 3), (1, 15), (2, 15), (1, 10), (2, 10), (2, 4), (4, 4), (3, 5), (4, 5)],
    )
    @allure.title("Пагинация в списке пользователей")
    def test_pagination_users_list(self, page, size, all_users, users_request):
        total = all_users["total"]

        response = users_request.get_users_list({"page": page, "size": size})
        assert_helpers.check_status_code(response, 200)

        response = response.json()
        response_user = response["items"]
        total_pages = ceil(total / size)
        last_page = total % size
        per_page = size % total
        current_length = last_page if page == total_pages and last_page != 0 else size

        assert response["total"] == total
        assert response["page"] == page
        assert response["size"] == size
        assert response["pages"] == total_pages
        if page <= total_pages:
            start_id = (page - 1) * per_page
            x = all_users["items"][start_id : start_id + current_length]
            assert len(response_user) == current_length
            assert response_user == x
        else:
            assert len(response_user) == 0
