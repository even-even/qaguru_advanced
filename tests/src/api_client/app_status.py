from requests import Response

from data.strings import APP_URL
from tests.src.api_client.base_client import BaseApiRequest


class AppStatusRequest(BaseApiRequest):
    BASE_USERS_URL = APP_URL
    STATUS = "/status/"

    def get_status(self, url=BASE_USERS_URL) -> Response:
        return self.get(
            url=url,
            path=self.STATUS)
