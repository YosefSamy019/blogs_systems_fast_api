# from typing import Optional
# from pydantic import BaseModel
#
# from fastapi import FastAPI
# import uvicorn
#
# app = FastAPI()
#
# """
# operations:
# GET
# POST -> create
# PUT -> update
# DELETE
#
# """
#
#
# @app.get("/")
# def index():
#     return {
#         "data": "Blog List",
#         "status": "success",
#     }
#
#
# @app.get("/blog")
# def blog(
#         limit: int = 10,
#         published: bool = False,
#         sort: Optional[str] = None,
# ):
#     return {
#         "data": f"{limit} blogs only, published {published}, optionally sort by {sort}",
#         "status": "success",
#     }
#
#
# @app.get("/blog/unpublished")
# def unpublish():
#     return {
#         "data": "all unpublished blogs",
#         "status": "success",
#     }
#
#
# @app.get("/blog/{id}")
# def show(id: int):
#     return {
#         "data": id,
#         "status": "success",
#     }
#
#
# @app.get("/blog/{id}/comments")
# def comments(
#         id: int,
#         limit: int = 10,
# ):
#     return {
#         "data": f"comments, limit by {limit} ",
#         "status": "success",
#     }
#
#
# class BlogCreate(BaseModel):
#     title: str
#     body: str
#     published_at: Optional[bool]
#
#
# @app.post("/blog")
# def create_blog(
#         request: BlogCreate,
# ):
#     return {
#         "data": f"Blog created {request.title}, {request.body}, published {request.published_at}",
#         "status": "success",
#     }
#
#
# # For debugging purpose
# # if __name__ == "__main__":
# #     uvicorn.run(app, host="127.0.0.1", port=8000)
