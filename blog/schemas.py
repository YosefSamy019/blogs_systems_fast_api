from typing import List

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str


class Blog(BaseModel):
    title: str
    body: str


class ShowUser(BaseModel):
    username: str
    email: str
    blogs: List[Blog]

    class Config:
        orm_mode = True


class ShowBlog(Blog):
    class Config:
        orm_mode = True  # ORM mode

    creator: ShowUser
