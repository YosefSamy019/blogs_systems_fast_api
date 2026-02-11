from typing import List

from fastapi import FastAPI, status, HTTPException, Response, APIRouter
from fastapi.params import Depends

from sqlalchemy.orm import Session

from app import schemas, database, models
from app.hashing import Hash
import app.repository.user as user_repo

user_router = APIRouter(
    tags=['user'],
    prefix="/user",
)


@user_router.post("/{user_id}",
                  status_code=status.HTTP_201_CREATED,
                  response_model=schemas.ShowUser
                  )
async def create_user(
        request: schemas.User,
        user_id: int,
        db: Session = Depends(database.get_db),
):
    return user_repo.create(db, request)


@user_router.get("/{user_id}",
                 status_code=status.HTTP_200_OK,
                 response_model=schemas.ShowUser)
async def get_user(
        user_id: int,
        db: Session = Depends(database.get_db),
):
    return user_repo.get(db, user_id)
