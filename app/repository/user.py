from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models
from app.hashing import Hash


def create(
        db: Session,
        request
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


def get(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} doesn't exist",
        )
    return user
