from sqlmodel import Session, select

from board.domain.comment.comment import Comment
from board.domain.comment.comment_repository import CommentRepository
from board.infrastructure.persistence.mappers.sqlmodel.comment_mapper import (
    SQLModelCommentMapper,
)
from .models import CommentModel


class SQLModelCommentRepository(CommentRepository):
    def __init__(self, session: Session):
        self.session = session
        self.mapper = SQLModelCommentMapper()

    def save(self, comment: Comment) -> Comment:
        db_comment = self.mapper.to_orm(comment)
        self.session.add(db_comment)
        self.session.commit()
        self.session.refresh(db_comment)
        return self.mapper.to_domain(db_comment)

    def find_by_id(self, id: int) -> Comment | None:
        statement = select(CommentModel).where(CommentModel.id == id)
        db_comment = self.session.exec(statement).first()
        return self.mapper.to_domain(db_comment) if db_comment else None

    def find_by_post_id(self, post_id: int) -> list[Comment]:
        statement = select(CommentModel).where(CommentModel.post_id == post_id)
        db_comments = self.session.exec(statement).all()
        return [self.mapper.to_domain(db_comment) for db_comment in db_comments]

    def update(self, comment: Comment) -> Comment:
        db_comment = self.session.get(CommentModel, comment.id)
        if db_comment:
            updated_db_comment = self.mapper.to_orm(comment)
            for key, value in updated_db_comment.__dict__.items():
                setattr(db_comment, key, value)
            self.session.add(db_comment)
            self.session.commit()
            self.session.refresh(db_comment)
        return self.mapper.to_domain(db_comment)

    def delete(self, id: int) -> None:
        db_comment = self.session.get(CommentModel, id)
        if db_comment:
            self.session.delete(db_comment)
            self.session.commit()
