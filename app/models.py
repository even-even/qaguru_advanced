from datetime import datetime

from pydantic import BaseModel


# Базовая модель пользователя
class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


# Модель для создания пользователя
class UserCreate(BaseModel):
    name: str
    job: str


# Модель для обновления пользователя
class UserUpdate(BaseModel):
    name: str | None = None
    job: str | None = None
    email: str | None = None


# Модель ответа при успешном создании пользователя
class ResponseUserCreate(User):
    created_at: datetime


# Модель ответа при успешном обновлении пользователя
class ResponseUserUpdate(User):
    updated_at: datetime
