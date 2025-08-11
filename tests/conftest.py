import time
from multiprocessing import Process

import pytest
import requests
import uvicorn
from loguru import logger

from app.main import app
from tests.src.allure_decorators import After, Given
from tests.src.api_client.users import UsersRequest


def _run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)


@pytest.fixture(scope="session")
def server():
    with Given("Сервер запущен"):
        process = Process(target=_run_server, daemon=True)
        process.start()

        # Ждем пока сервер станет доступен
        url = "http://localhost:8000/api/users"
        for _ in range(10):
            try:
                if requests.get(url, timeout=45).status_code < 500:
                    break
            except requests.RequestException as e:
                logger.error(f"Ошибка подключения к серверу: {e}")
            time.sleep(0.5)
        else:
            msg = "Сервер не запустился"
            raise RuntimeError(msg)

    yield
    with After("Сервер выключен"):
        process.terminate()


@pytest.fixture(scope="session")
def users_request() -> UsersRequest:
    return UsersRequest()
