from typing import Optional

from sqlmodel import Session, select

from board.domain.post.post import Post
from board.domain.post.post_repository import PostRepository
from board.infrastructure.persistence.mappers.sqlmodel.post_mapper import (
    SQLModelPostMapper,
)
from .models import PostModel


class SQLModelPostRepository(PostRepository):
    def __init__(self, session: Session):
        self.session = session
        self.mapper = SQLModelPostMapper()

    def save(self, post: Post) -> Post:
        db_post = self.mapper.to_orm(post)
        self.session.add(db_post)
        self.session.commit()
        self.session.refresh(db_post)
        return self.mapper.to_domain(db_post)

    def find_by_id(self, id: int) -> Optional[Post]:
        statement = select(PostModel).where(PostModel.id == id)
        db_post = self.session.exec(statement).first()
        return self.mapper.to_domain(db_post) if db_post else None

    def find_all(self, skip: int = 0, limit: int = 100) -> list[Post]:
        statement = select(PostModel).offset(skip).limit(limit)
        db_posts = self.session.exec(statement).all()
        return [self.mapper.to_domain(db_post) for db_post in db_posts]

    def update(self, post: Post) -> Post:
        db_post = self.session.get(PostModel, post.id)
        if db_post:
            updated_db_post = self.mapper.to_orm(post)
            for key, value in updated_db_post.dict().items():
                setattr(db_post, key, value)
            self.session.add(db_post)
            self.session.commit()
            self.session.refresh(db_post)
        return self.mapper.to_domain(db_post)

    def delete(self, id: int) -> None:
        db_post = self.session.get(PostModel, id)
        if db_post:
            self.session.delete(db_post)
            self.session.commit()

    def search(self, query: str) -> list[Post]:
        statement = select(PostModel).where(
            (PostModel.title.contains(query)) | (PostModel.content.contains(query))
        )
        db_posts = self.session.exec(statement).all()
        return [self.mapper.to_domain(db_post) for db_post in db_posts]
