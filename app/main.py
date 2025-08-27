from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import dotenv
from fastapi_pagination import add_pagination

dotenv.load_dotenv()  # нужно инитить в самом начале


import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.database.engine import create_db_and_tables
from app.routes import status, users


# аналог фикстуры - выполняется до и после запуска сервиса
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:  # noqa: RUF029
    logger.debug("On startup")

    create_db_and_tables()

    yield
    logger.debug("On shutdown")


app = FastAPI(lifespan=lifespan)

add_pagination(app)
app.include_router(status.router)
app.include_router(users.router)


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
