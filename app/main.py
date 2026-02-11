from fastapi import FastAPI

import app.database as database
from app import models
from app.routers.blog import blog_router
from app.routers.login import login_router
from app.routers.user import user_router

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(
    router=login_router
)

app.include_router(
    router=blog_router
)
app.include_router(
    router=user_router
)
