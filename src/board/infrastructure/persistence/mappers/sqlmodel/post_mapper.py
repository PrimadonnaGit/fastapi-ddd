from datetime import datetime

from board.domain.post.post import Post
from board.domain.post.post_aggregate import PostAggregate
from board.infrastructure.persistence.mappers.base import BaseMapper
from board.infrastructure.persistence.sqlmodel.models import PostModel


class SQLModelPostMapper(BaseMapper[Post, PostModel]):
    @staticmethod
    def to_domain(db_post: PostModel) -> Post:
        return Post(
            id=db_post.id,
            title=db_post.title,
            content=db_post.content,
            is_admin_post=db_post.is_admin_post,
            views=db_post.views,
            created_at=db_post.created_at,
            updated_at=db_post.updated_at,
            category_id=db_post.category_id,
            user_id=db_post.user_id,
            tags=[],
        )

    @staticmethod
    def to_orm(post: Post) -> PostModel:
        return PostModel(
            id=post.id,
            title=post.title,
            content=post.content,
            is_admin_post=post.is_admin_post,
            views=post.views,
            created_at=post.created_at or datetime.utcnow(),
            updated_at=post.updated_at,
            category_id=post.category_id,
            user_id=post.user_id,
        )

    @staticmethod
    def to_aggregate(db_post: PostModel) -> PostAggregate:
        post = SQLModelPostMapper.to_domain(db_post)
        return PostAggregate(post)
