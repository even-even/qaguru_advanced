from pydantic import BaseModel


# Базовая модель проверки состояния сервиса
class AppStatus(BaseModel):
    status: bool
