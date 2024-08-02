from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session
from starlette import status
from starlette.exceptions import HTTPException

from board.application.category.category_service import CategoryApplicationService
from board.application.comment.comment_service import CommentApplicationService
from board.application.file.file_service import FileApplicationService
from board.application.post.post_service import PostApplicationService
from board.application.user.user_service import UserApplicationService
from board.domain.category.category_repository import CategoryRepository
from board.domain.comment.comment_repository import CommentRepository
from board.domain.file.file_repository import FileRepository
from board.domain.post.post_repository import PostRepository
from board.domain.user.user_repository import UserRepository
from core.config import settings
from core.di_container import Container

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

container = Container()


def get_db_session() -> Session:
    with container.db_session() as session:
        yield session


def get_user_repository(
    session: Annotated[Session, Depends(get_db_session)]
) -> UserRepository:
    return container.user_repository(session=session)


def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserApplicationService:
    return container.user_application_service(user_repository=user_repository)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: Annotated[UserApplicationService, Depends(get_user_service)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user


def get_category_repository(
    session: Annotated[Session, Depends(get_db_session)]
) -> CategoryRepository:
    return container.category_repository(session=session)


def get_category_service(
    category_repository: Annotated[
        CategoryApplicationService, Depends(get_category_repository)
    ]
) -> CategoryApplicationService:
    return container.category_application_service(
        category_repository=category_repository
    )


def get_post_repository(db: Session = Depends(get_db_session)) -> PostRepository:
    return Container().post_repository(session=db)


def get_post_service(
    post_repository: Annotated[PostRepository, Depends(get_post_repository)]
) -> PostApplicationService:
    return Container().post_application_service(post_repository=post_repository)


def get_comment_repository(db: Session = Depends(get_db_session)) -> CommentRepository:
    return Container().comment_repository(session=db)


def get_comment_service(
    comment_repository: Annotated[CommentRepository, Depends(get_comment_repository)]
) -> CommentApplicationService:
    return Container().comment_application_service(
        comment_repository=comment_repository
    )


def get_file_repository(db: Session = Depends(get_db_session)) -> FileRepository:
    return Container().file_repository(session=db)


def get_file_service(
    file_repository: Annotated[FileRepository, Depends(get_file_repository)]
) -> FileApplicationService:
    return Container().file_application_service(file_repository=file_repository)
