import time
from http import HTTPStatus
from multiprocessing import Process

import pytest
import requests
import uvicorn
from loguru import logger

from app.main import app
from tests.src.allure_decorators import After, Given
from tests.src.api_client.users import UsersRequest


@pytest.fixture(scope="function")
def users_list():
    response = UsersRequest().get_users_list()
    assert response.status_code == HTTPStatus.OK
    return response.json()


def _run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)


@pytest.fixture(scope="session")
def server():
    with Given("Сервер запущен"):
        process = Process(target=_run_server, daemon=True)
        process.start()

        # Ждем пока сервер станет доступен
        url = "http://0.0.0.0:8000/api/users/"

        for _ in range(10):
            time.sleep(1)
            try:
                if requests.get(url, timeout=45).status_code < 500:
                    break
            except requests.RequestException as e:
                logger.error(f"Ошибка подключения к серверу: {e}")
        else:
            msg = "Сервер не запустился"
            raise RuntimeError(msg)

    yield
    with After("Сервер выключен"):
        process.terminate()
