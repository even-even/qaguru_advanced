# База данных в памяти
# 09.08.2025 TODO: заюзать БД вместо хардкода
from app.models import User

db: dict[int, User] = {
    1: User(
        id=1,
        email="george.bluth@reqres.in",
        first_name="George",
        last_name="Bluth",
        avatar="https://reqres.in/img/faces/1-image.jpg",
    ),
    2: User(
        id=2,
        email="janet.weaver@reqres.in",
        first_name="Janet",
        last_name="Weaver",
        avatar="https://reqres.in/img/faces/2-image.jpg",
    ),
    11: User(
        id=11,
        email="george.edwards@reqres.in",
        first_name="George",
        last_name="Edwards",
        avatar="https://reqres.in/img/faces/11-image.jpg",
    ),
    12: User(
        id=12,
        email="rachel.howell@reqres.in",
        first_name="Rachel",
        last_name="Howell",
        avatar="https://reqres.in/img/faces/12-image.jpg",
    ),
}

jobs_db: dict[int, str] = {}
