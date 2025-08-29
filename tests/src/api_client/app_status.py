from httpx import Response

from data.strings import APP_URL
from tests.src.api_client.base_client import BaseApiRequest


class AppStatusRequest(BaseApiRequest):
    STATUS = "/status/"

    def get_status(self, url=APP_URL) -> Response:
        return self.get(
            url=url,
            path=self.STATUS)
