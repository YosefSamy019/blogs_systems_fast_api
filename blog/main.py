from typing import List

from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Depends

from blog.database import SessionLocal
from blog.hashing import Hash
from blog.schemas import Blog
import blog.database as database
from blog import models, schemas
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

from passlib.context import CryptContext


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/blogs",
         tags=['blog'],
         response_model=List[schemas.ShowBlog],  # Select Response Scheme, auto remove id field
         )
async def all_blogs(
        db: Session = Depends(get_db),
):
    blogs = db.query(models.Blog).all()
    return blogs


@app.post("/blog",
          tags=['blog'],
          status_code=status.HTTP_201_CREATED)
async def create(
        request: Blog,
        db: Session = Depends(get_db)  # Not query Param
):
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=1
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.get("/blog/{blog_id}",
         tags=['blog'],
         status_code=status.HTTP_200_OK,
         response_model=schemas.ShowBlog  # Show Response Model Schema in docs
         )
async def get_blog(
        blog_id: int,
        response: Response,  # to change status code
        db: Session = Depends(get_db),
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


@app.delete("/blog/{blog_id}",
            tags=['blog'],
            status_code=status.HTTP_200_OK)
async def delete_blog(
        blog_id: int,
        db: Session = Depends(get_db),
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} doesn't exist",
        )

    db.query(models.Blog).filter(models.Blog.id == blog_id).delete(
        synchronize_session=False
    )
    db.commit()
    return {
        "message": f"Blog with id {blog_id} has been deleted",
    }


@app.put("/blog/{blog_id}",
         tags=['blog'],
         status_code=status.HTTP_202_ACCEPTED)
async def update_blog(
        blog_id: int,
        request: schemas.Blog,
        db: Session = Depends(get_db),
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} doesn't exist",
        )

    db.query(models.Blog).filter(models.Blog.id == blog_id).update(
        {
            "title": request.title,
            "body": request.body,
        }
    )
    db.commit()

    return {
        "message": f"Blog with id {blog_id} has been updated",
    }


@app.post("/user/{user_id}",
          tags=['user'],
          status_code=status.HTTP_201_CREATED,
          response_model=schemas.ShowUser
          )
async def create_user(
        request: schemas.User,
        db: Session = Depends(get_db),
):
    hashed_password = Hash().bcrypt(password=request.password)

    new_user = models.User(
        username=request.username,
        email=request.email,
        password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/user/{user_id}",
         tags=['user'],
         status_code=status.HTTP_200_OK,
         response_model=schemas.ShowUser)
async def get_user(
        user_id: int,
        db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} doesn't exist",
        )
    return user
