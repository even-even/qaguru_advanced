import json
from pathlib import Path

from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check

from app.models.user import User, UserCreate, UserUpdate

# Отключаем предупреждения о расширениях
disable_installed_extensions_check()

router = APIRouter()
USERS_FILE = Path(__file__).parent.parent.parent / "data" / "users.json"


def load_users() -> list[User]:
    """Загружаем пользователей из JSON файла"""
    try:
        if not USERS_FILE.exists():
            USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
            USERS_FILE.write_text("[]")
            return []

        return [User(**user) for user in json.loads(USERS_FILE.read_text())]
    except json.JSONDecodeError:
        return []


def save_users(users: list[User]) -> None:
    """Сохраняем пользователей в JSON файл"""
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    USERS_FILE.write_text(json.dumps([user.model_dump() for user in users], indent=2))


@router.post("/api/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> dict:
    users = load_users()
    new_id = max([u.id for u in users], default=0) + 1

    new_user = User(
        id=new_id,
        email=user.email or f"{user.name.lower()}@example.com",
        first_name=user.name,
        last_name="",
        avatar=f"https://reqres.in/img/faces/{new_id}-image.jpg",
    )

    users.append(new_user)
    save_users(users)
    return {"id": new_id, "name": user.name, "email": new_user.email, "job": getattr(user, "job", "")}


@router.get("/api/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int) -> User:
    users = load_users()

    if user_id < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Invalid user_id {user_id}")
    if user_id > len(users):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
    return users[user_id - 1]


@router.get("/api/users/", status_code=status.HTTP_200_OK)
def get_users_list() -> Page[User]:
    users = load_users()
    return paginate(users)


@router.put("/api/users/{user_id}/")
async def update_user(user_id: int, user_data: UserUpdate) -> dict:
    users = load_users()
    user_index = next((i for i, u in enumerate(users) if u.id == user_id), None)

    if user_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user = users[user_index]
    if user_data.name:
        user.first_name = user_data.name
    if user_data.email:
        user.email = user_data.email

    save_users(users)
    return {"name": user.first_name, "email": user.email}


@router.delete("/api/users/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int) -> None:
    users = load_users()
    updated_users = [u for u in users if u.id != user_id]

    if len(updated_users) == len(users):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    save_users(updated_users)
