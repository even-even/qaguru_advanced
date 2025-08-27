import json
from pathlib import Path

import pytest

from app.models.user import UserCreate
from data.strings import BLACK_LIST_CODES
from tests.src import assert_helpers
from tests.src.allure_decorators import After, Given
from tests.src.data_generators import get_random_string
from tests.src.files_helper import get_root_path


@pytest.fixture(scope="session")
def fill_test_data(users_request):
    """Фикстура для заполнения тестовых данных"""
    with Given("БД заполнена значениями"):
        with Path(f"{get_root_path()}/data/users.json").open(encoding="utf-8") as json_file:
            test_data_users = json.load(json_file)

        api_users = []
        for user in test_data_users:
            response = users_request.create_user(json=user)
            api_users.append(response.json())

        user_ids = [user["id"] for user in api_users]
        yield user_ids

        with After("Очистить БД после тестовой сессии"):
            for user_id in user_ids:
                users_request.delete_user(user_id)


@pytest.fixture(scope="function")
def users_list(users_request):
    """Список пользователей"""
    response = users_request.get_users_list()
    assert_helpers.check_status_code(response, 200)
    return response.json()


@pytest.fixture(scope="function")
def create_user(users_request):
    """Создание нового пользователя"""
    with Given("Создан новый пользователь"):
        user = UserCreate(
            email=f"{get_random_string().lower()}@autotest.ru",
            first_name=f"first_name_{get_random_string()}",
            last_name=f"last_name{get_random_string()}",
            avatar=f"http://avatar_autotest.ru/{get_random_string().lower()}"
        ).model_dump()

        response = users_request.create_user(user)
        assert_helpers.check_status_code(response, 201)
        user_object = response.json()
        user_id = user_object["id"]

    yield user_object

    with After(f"Удалить пользователя {user_id} после окончания теста"):
        r_deactivate = users_request.delete_user(user_id)
        assert_helpers.check_not_status_code_in_list(r_deactivate, BLACK_LIST_CODES)
