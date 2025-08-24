from httpx import Response

from data.strings import APP_URL
from tests.src.api_client.base_client import BaseApiRequest


class UsersRequest(BaseApiRequest):
    USERS = "/api/users/"

    def get_users_list(self, params: dict | None = None, url=APP_URL) -> Response:
        return self.get(
            url=url,
            path=self.USERS,
            params=params)

    def get_user_by_id(self, user_id: int, url=APP_URL) -> Response:
        return self.get(
            url=url,
            path=f"{self.USERS}{user_id}")

    def create_user(self, json: dict, url=APP_URL) -> Response:
        return self.post(
            url=url,
            path=self.USERS,
            json=json)

    def delete_user(self, user_id: int, url=APP_URL) -> Response:
        return self.delete(
            url=url,
            path=f"{self.USERS}{user_id}")

    def patch_user(self, user_id: int, json: dict, url=APP_URL) -> Response:
        return self.patch(
            url=url,
            path=f"{self.USERS}{user_id}",
            json=json)
