import json
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.models.user import User
from app.routes import status, users
from tests.src.files_helper import get_root_path

app = FastAPI()
add_pagination(app)

app.include_router(users.router)
app.include_router(status.router)


# Загрузка данных из JSON файла
def load_users_from_json() -> dict:
    with Path(f"{get_root_path()}/data/users.json").open(encoding="utf-8") as json_file:
        return json.load(json_file)


users_list = load_users_from_json()  # Загружаем пользователей при старте

if __name__ == "__main__":
    for user in users_list:
        User.model_validate(user)

    uvicorn.run(app, host="0.0.0.0", port=8000)
