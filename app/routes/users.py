from collections.abc import Iterable

from fastapi import APIRouter, HTTPException, status

from app.database import users
from app.models.user import User, UserCreate, UserUpdate

router = APIRouter(prefix="/api/users")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: User) -> User:
    UserCreate.model_validate(user.model_dump())  # явно валидируем входные параметры
    return users.create_user(user)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int) -> User:

    if user_id < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Invalid user_id {user_id}")
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
    return user


@router.get("/", status_code=status.HTTP_200_OK)
def get_users_list() -> Iterable[User]:
    return users.get_users_list()


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, patch_data: UserUpdate) -> User:
    """ Частичное обновление данных пользователя по заданному ID"""
    if user_id < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Неверный user_id {user_id}")

    # Получаем текущего пользователя из базы данных
    current_user = users.get_user(user_id)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с ID {user_id} не найден.")

    # Применяем обновление
    for key, value in patch_data.model_dump(exclude_unset=True).items():  # Исключаем необновляемые поля
        setattr(current_user, key, value)

    # Сохраняем изменения в базе данных

    return users.update_user(user_id, current_user)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)  # если 204, то не должно быть сообщения в return
async def delete_user(user_id: int) -> dict[str, str]:
    if user_id < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Invalid user_id {user_id}")
    users.delete_user(user_id)
    return {"message": f"User {user_id} deleted"}
