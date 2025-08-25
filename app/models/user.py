from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


# Базовая модель пользователя
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, ge=1)  # None т.к. id может не быть в БД перед операцией
    email: EmailStr
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    avatar: str | None  # Используем простую строку для аватарки, так как HttpUrl не поддерживается SQLModel


# Модель для создания пользователя
class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str


# Модель для обновления пользователя
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar: str | None = None
