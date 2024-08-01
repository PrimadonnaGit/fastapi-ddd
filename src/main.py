from fastapi import FastAPI
from sqlmodel import SQLModel

from board.interfaces.api.v1 import (
    user_routes,
    category_routes,
    post_routes,
    comment_routes,
    file_routes,
)
from core.config import settings
from core.di_container import Container

app = FastAPI(title=settings.PROJECT_NAME)
container = Container()

app.container = container

app.include_router(user_routes.router, prefix="/api/v1/users", tags=["users"])
app.include_router(
    category_routes.router, prefix="/api/v1/categories", tags=["categories"]
)
app.include_router(post_routes.router, prefix="/api/v1/posts", tags=["posts"])
app.include_router(comment_routes.router, prefix="/api/v1/comments", tags=["comments"])
app.include_router(file_routes.router, prefix="/api/v1/files", tags=["files"])


@app.on_event("startup")
def on_startup():
    container.wire(
        modules=[
            "board.interfaces.api.v1.user_routes",
            "board.interfaces.api.v1.category_routes",
            "board.interfaces.api.v1.post_routes",
            "board.interfaces.api.v1.comment_routes",
            "board.interfaces.api.v1.file_routes",
        ]
    )
    SQLModel.metadata.create_all(container.db_engine())


@app.on_event("shutdown")
async def on_shutdown():
    container.db_engine().dispose()


# @app.middleware("http")
# async def db_session_middleware(request, call_next):
#     session = next(get_db_session())
#     try:
#         response = await call_next(request)
#     finally:
#         session.close()
#     return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)