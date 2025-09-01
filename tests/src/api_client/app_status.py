from httpx import Response

from tests.src.api_client.base_client import BaseApiRequest


class AppStatusRequest(BaseApiRequest):
    STATUS = "/status/"

    def get_status(self) -> Response:
        return self.get(
            path=self.STATUS)
