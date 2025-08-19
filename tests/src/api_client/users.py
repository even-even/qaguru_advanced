from httpx import Response

from tests.src.api_client.base_client import BaseApiRequest


class UsersRequest(BaseApiRequest):
    BASE_USERS_URL = "http://0.0.0.0:8000"
    USERS = "/api/users/"

    def get_users_list(self, params: dict | None = None, url=BASE_USERS_URL) -> Response:
        return self.get(
            url=url,
            path=self.USERS,
            params=params)

    def get_user_by_id(self, user_id: int, url=BASE_USERS_URL) -> Response:
        return self.get(
            url=url,
            path=f"{self.USERS}{user_id}")

    def create_user(self, json: dict, url=BASE_USERS_URL) -> Response:
        return self.post(
            url=url,
            path=self.USERS,
            json=json)

    def delete_user(self, user_id: int, url=BASE_USERS_URL) -> Response:
        return self.delete(
            url=url,
            path=f"{self.USERS}{user_id}/")

    def put_user_by_id(self, user_id: int, json: dict, url=BASE_USERS_URL) -> Response:
        return self.put(
            url=url,
            path=f"{self.USERS}{user_id}/",
            json=json)
