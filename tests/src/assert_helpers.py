from httpx import Response


def check_status_code(response: Response, status_code: int) -> None:
    """Проверка кода ответа с выводом тела в случае неуспеха"""
    assert response.status_code == status_code, (f"Ожидался status_code = {status_code},"
                                                 f" получен - {response} с текстом {response.text}")
