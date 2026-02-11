from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import app.models as models


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(db: Session, request):
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=1
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def destroy(db: Session, blog_id: int):
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


def update(
        db: Session,
        blog_id: int,
        request
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
