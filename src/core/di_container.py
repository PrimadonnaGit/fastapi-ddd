from dependency_injector import containers, providers
from sqlmodel import create_engine, Session

from board.application.category.category_service import CategoryApplicationService
from board.application.comment.comment_service import CommentApplicationService
from board.application.file.file_service import FileApplicationService
from board.application.post.post_service import PostApplicationService
from board.application.user.user_service import UserApplicationService
from board.infrastructure.persistence.sqlmodel.category_repository import (
    SQLModelCategoryRepository,
)
from board.infrastructure.persistence.sqlmodel.comment_repository import (
    SQLModelCommentRepository,
)
from board.infrastructure.persistence.sqlmodel.file_repository import (
    SQLModelFileRepository,
)
from board.infrastructure.persistence.sqlmodel.post_repository import (
    SQLModelPostRepository,
)
from board.infrastructure.persistence.sqlmodel.user_repository import (
    SQLModelUserRepository,
)
from .config import settings


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Database
    db_engine = providers.Singleton(create_engine, settings.DATABASE_URL)

    # Session
    db_session = providers.Factory(Session, bind=db_engine)

    # Repositories
    user_repository = providers.Factory(SQLModelUserRepository, session=db_session)
    category_repository = providers.Factory(
        SQLModelCategoryRepository, session=db_session
    )
    post_repository = providers.Factory(SQLModelPostRepository, session=db_session)
    comment_repository = providers.Factory(
        SQLModelCommentRepository, session=db_session
    )
    file_repository = providers.Factory(SQLModelFileRepository, session=db_session)

    # Application Services
    user_application_service = providers.Factory(
        UserApplicationService, user_repository=user_repository
    )
    category_application_service = providers.Factory(
        CategoryApplicationService, category_repository=category_repository
    )
    post_application_service = providers.Factory(
        PostApplicationService, post_repository=post_repository
    )
    comment_application_service = providers.Factory(
        CommentApplicationService, comment_repository=comment_repository
    )
    file_application_service = providers.Factory(
        FileApplicationService, file_repository=file_repository
    )
