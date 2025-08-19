from pydantic import BaseModel, EmailStr, PositiveInt


# Базовая модель пользователя
class User(BaseModel):
    id: PositiveInt
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str


# Модель для создания пользователя
class UserCreate(BaseModel):
    name: str
    email: str | None = None


# Модель для обновления пользователя
class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
