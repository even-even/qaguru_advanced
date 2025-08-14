from fastapi import APIRouter, status

from app.models.app_status import AppStatus
from app.models.user import User

router = APIRouter()

users: list[User] = []


@router.get("/status/", status_code=status.HTTP_200_OK)
async def get_status() -> AppStatus:
    return AppStatus(status=bool(users))
