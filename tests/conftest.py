import pytest

from tests.src.api_client.users import UsersRequest


@pytest.fixture(scope="session")
def users_request() -> UsersRequest:
    return UsersRequest()
