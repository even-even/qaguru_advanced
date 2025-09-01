from httpx import Response

from tests.src.api_client.base_client import BaseApiRequest


class UsersRequest(BaseApiRequest):
    """Клиент для работы эндпоинтами /api/users/"""

    USERS = "/api/users/"

    def get_users_list(self, params: dict | None = None) -> Response:
        return self.get(path=self.USERS, params=params)

    def get_user_by_id(self, user_id: int) -> Response:
        return self.get(path=f"{self.USERS}{user_id}")

    def create_user(self, json: dict) -> Response:
        return self.post(path=self.USERS, json=json)

    def delete_user(self, user_id: int) -> Response:
        return self.delete(path=f"{self.USERS}{user_id}")

    def patch_user(self, user_id: int, json: dict) -> Response:
        return self.patch(path=f"{self.USERS}{user_id}", json=json)
