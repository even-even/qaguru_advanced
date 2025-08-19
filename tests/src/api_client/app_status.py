from httpx import Response

from tests.src.api_client.base_client import BaseApiRequest


class AppStatusRequest(BaseApiRequest):
    BASE_USERS_URL = "http://0.0.0.0:8000"
    STATUS = "/status/"

    def get_status(self, url=BASE_USERS_URL) -> Response:
        return self.get(
            url=url,
            path=self.STATUS)
