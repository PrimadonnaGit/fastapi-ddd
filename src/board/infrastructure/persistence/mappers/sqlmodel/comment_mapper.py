from board.domain.comment.comment import Comment
from board.infrastructure.persistence.mappers.base import BaseMapper
from board.infrastructure.persistence.sqlmodel.models import CommentModel


class SQLModelCommentMapper(BaseMapper[Comment, CommentModel]):
    @staticmethod
    def to_domain(db_comment: CommentModel) -> Comment:
        return Comment(
            id=db_comment.id,
            content=db_comment.content,
            created_at=db_comment.created_at,
            updated_at=db_comment.updated_at,
            post_id=db_comment.post_id,
            user_id=db_comment.user_id,
            parent_comment_id=db_comment.parent_comment_id,
        )

    @staticmethod
    def to_orm(comment: Comment) -> CommentModel:
        return CommentModel(
            id=comment.id,
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            post_id=comment.post_id,
            user_id=comment.user_id,
            parent_comment_id=comment.parent_comment_id,
        )
