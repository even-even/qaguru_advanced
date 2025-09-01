from json import JSONDecodeError

import httpx
from curlify2 import Curlify
from loguru import logger

from tests.src.allure_decorators import Step
from tests.src.config.settings import AppSettings


class BaseApiRequest:
    """Базовый класс для выполнения HTTP-запросов."""

    def __init__(self, api_key: str | None = "reqres-free-v1", env: str | None = None) -> None:
        """Конструктор класса, устанавливает базовые параметры для выполнения запросов.

        :param api_key: Обязательный хедер
        :param env: Окружение на котором запускаются тесты (dev, stage, prod)
        """
        self.api_key = api_key

        # Создаем экземпляр настроек
        settings_kwargs = {}
        if env is not None:
            settings_kwargs["env"] = env

        self.settings = AppSettings(**settings_kwargs)
        self.base_url = self.settings.base_url  # Сохраняем базовый URL из настроек

    def request(self, method: str, url: str | None = None, path: str = "", *, headers: dict[str, str] | None = None,
                params: dict | None = None, data: dict | None = None, json: dict | None = None,
                files: dict | None = None) -> httpx.Response:
        """Общий метод для выполнения HTTP-запросов."""
        final_headers = headers.copy() if headers else {}
        if self.api_key:
            final_headers["x-api-key"] = self.api_key

        # Используем base_url из настроек, если url не указан явно
        if url is None:
            url = self.base_url

        full_url = f"{url}{path}"

        with Step(f"Выполнить {method.upper()} запрос {full_url}"):
            kwargs_to_pass = {
                "headers": final_headers,
                "params": params or {},
                "verify": False,
                "timeout": (45, 45),
            }

            if method.lower() in ("post", "put", "patch"):
                kwargs_to_pass.update({
                    "json": json,
                    "data": data,
                })

            if method.lower() == "post":
                kwargs_to_pass["files"] = files

            result = getattr(httpx, method.lower())(
                url=full_url, **kwargs_to_pass)

            _log_request_result(result)
            return result

    def get(self, path: str, url: str | None = None, params: dict | None = None) -> httpx.Response:
        return self.request(method="GET", url=url, path=path, params=params)

    def post(self, path: str, url: str | None = None, params: dict | None = None, data: dict | None = None,
             json: dict | None = None, files: dict | None = None) -> httpx.Response:
        return self.request(
            method="POST", url=url, path=path, params=params, data=data, json=json, files=files)

    def patch(self, path: str, url: str | None = None, data: dict | None = None, json: dict | None = None,
              params: dict | None = None) -> httpx.Response:
        return self.request(method="PATCH", url=url, path=path, data=data, json=json, params=params)

    def put(self, path: str, url: str | None = None, data: dict | None = None,
            json: dict | None = None) -> httpx.Response:
        return self.request(method="PUT", url=url, path=path, data=data, json=json)

    def delete(self, path: str, url: str | None = None, params: dict | None = None) -> httpx.Response:
        return self.request(method="DELETE", url=url, path=path, params=params)


def _log_request_result(response: httpx.Response) -> None:
    """Логируем информацию о запросе/ответе"""
    request_message = f"\n\t|> Запрос:\n\t{Curlify(response.request).to_curl()}\n\t"

    try:
        log_msg = (
            f"{request_message}"
            f"|> Ответ:\n\t{str(response.json())[:1500]}\n\t"
            f"|> Статус-код: {response.status_code}"
        )
        logger.info(log_msg)
    except JSONDecodeError:
        log_msg = (
            f"{request_message}"
            f"|> Ответ: {response.text}\n\t"
            f"|> Статус-код: {response.status_code}"
        )
        logger.info(log_msg)
