from fastapi import APIRouter, Depends

from typing import List

from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Depends

from app import oauth
from app.schemas import Blog
import app.database as database

from app.repository import blog
from app import models, schemas
from sqlalchemy.orm import Session

blog_router = APIRouter(
    tags=['blog'],
    prefix="/blog",
)


@blog_router.get("/all",
                 response_model=List[schemas.ShowBlog],  # Select Response Scheme, auto remove id field
                 )
async def all_blogs(
        db: Session = Depends(database.get_db),
        current_user: schemas.User = Depends(
            oauth.get_current_user
        )
):
    blogs = blog.get_all(db)
    return blogs


@blog_router.post("/",
                  status_code=status.HTTP_201_CREATED)
async def create(
        request: Blog,
        current_user: schemas.User = Depends(
            oauth.get_current_user
        ),
        db: Session = Depends(database.get_db)  # Not query Param
):
    return blog.create(db, request)


@blog_router.get("/{blog_id}",
                 status_code=status.HTTP_200_OK,
                 response_model=schemas.ShowBlog  # Show Response Model Schema in docs
                 )
async def get_blog(
        blog_id: int,
        response: Response,  # to change status code
        current_user: schemas.User = Depends(
            oauth.get_current_user
        ),
        db: Session = Depends(database.get_db),
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

    # if not blog:
    #     response.status_code = status.HTTP_404_NOT_FOUND

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} doesn't exist",
        )

    return blog


@blog_router.delete("/{blog_id}",
                    status_code=status.HTTP_200_OK)
async def delete_blog(
        blog_id: int,
        db: Session = Depends(database.get_db),
        current_user: schemas.User = Depends(
            oauth.get_current_user
        ),
):
    return blog.destroy(
        db,
        blog_id,
    )


@blog_router.put("/{blog_id}",
                 status_code=status.HTTP_202_ACCEPTED)
async def update_blog(
        blog_id: int,
        request: schemas.Blog,
        db: Session = Depends(database.get_db),
        current_user: schemas.User = Depends(
            oauth.get_current_user
        ),
):
    return blog.update(
        db,
        blog_id,
        request,
    )
