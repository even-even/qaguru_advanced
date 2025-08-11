
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Query

from app.database import db, jobs_db
from app.models import User, UserCreate, UserUpdate
from tests.src.strings import USER_NOT_FOUND

router = APIRouter()


@router.post("/api/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> dict:
    new_id = max(db.keys()) + 1 if db else 1
    new_user = User(
        id=new_id,
        email=f"{user.name.lower()}@example.com",
        first_name=user.name,
        last_name="",
        avatar=f"https://reqres.in/img/faces/{new_id}-image.jpg",
    )
    db[new_id] = new_user
    jobs_db[new_id] = user.job
    return {"id": new_id, "name": user.name, "job": user.job}


@router.get("/api/users/{user_id}/")
async def get_user_by_id(user_id: int) -> User:
    if user_id not in db:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
    return db[user_id]


@router.get("/api/users/")
async def get_users(limit: int = Query(10), offset: int = Query(0)) -> list[User]:
    users = list(db.values())
    return users[offset: offset + limit]


@router.put("/api/users/{user_id}/")
async def update_user(user_id: int, user_data: UserUpdate) -> dict:
    if user_id not in db:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)

    user = db[user_id]
    if user_data.name:
        user.first_name = user_data.name
    if user_data.email:
        user.email = user_data.email
    if user_data.job:
        jobs_db[user_id] = user_data.job

    return {"name": user.first_name, "job": jobs_db.get(user_id, ""), "email": user.email}


@router.delete("/api/users/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int) -> None:
    if user_id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND)
    db.pop(user_id)
    jobs_db.pop(user_id, None)
