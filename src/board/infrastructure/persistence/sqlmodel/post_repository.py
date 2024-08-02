from sqlmodel import Session, select

from board.domain.post.post_aggregate import PostAggregate
from board.domain.post.post_repository import PostRepository
from .models import PostModel, CommentModel, FileModel
from ..mappers.sqlmodel.comment_mapper import SQLModelCommentMapper
from ..mappers.sqlmodel.file_mapper import SQLModelFileMapper
from ..mappers.sqlmodel.post_mapper import SQLModelPostMapper


class SQLModelPostRepository(PostRepository):
    def __init__(self, session: Session):
        self.session = session
        self.post_mapper = SQLModelPostMapper()
        self.comment_mapper = SQLModelCommentMapper()
        self.file_mapper = SQLModelFileMapper()

    def save(self, post_aggregate: PostAggregate) -> PostAggregate:
        db_post = self.post_mapper.to_orm(post_aggregate.post)
        self.session.add(db_post)

        for comment in post_aggregate.comments:
            db_comment = self.comment_mapper.to_orm(comment)
            self.session.add(db_comment)

        for file in post_aggregate.files:
            db_file = self.file_mapper.to_orm(file)
            self.session.add(db_file)

        self.session.commit()
        self.session.refresh(db_post)

        return self.find_by_id(db_post.id)

    def find_by_id(self, post_id: int) -> PostAggregate | None:
        db_post = self.session.get(PostModel, post_id)
        if not db_post:
            raise ValueError("Post not found")

        post = self.post_mapper.to_domain(db_post)
        post_aggregate = PostAggregate(post)

        comments = self.session.exec(
            select(CommentModel).where(CommentModel.post_id == post_id)
        ).all()
        post_aggregate.comments = [self.comment_mapper.to_domain(c) for c in comments]

        files = self.session.exec(
            select(FileModel).where(FileModel.post_id == post_id)
        ).all()
        post_aggregate.files = [self.file_mapper.to_domain(f) for f in files]

        return post_aggregate

    def find_all(self, skip: int = 0, limit: int = 100) -> list[PostAggregate]:
        statement = select(PostModel).offset(skip).limit(limit)
        db_posts = self.session.exec(statement).all()
        return [self.mapper.to_domain(db_post) for db_post in db_posts]

    def delete(self, post_id: int) -> None:
        db_post = self.session.get(PostModel, post_id)
        if db_post:
            self.session.delete(db_post)
            self.session.commit()

    def search(self, query: str, skip: int = 0, limit: int = 20) -> list[PostAggregate]:
        statement = (
            select(PostModel)
            .where(
                (PostModel.title.contains(query)) | (PostModel.content.contains(query))
            )
            .offset(skip)
            .limit(limit)
        )

        db_posts = self.session.exec(statement).all()

        post_aggregates = []
        for db_post in db_posts:
            post = self.post_mapper.to_domain(db_post)
            post_aggregate = PostAggregate(post)

            comments = self.session.exec(
                select(CommentModel).where(CommentModel.post_id == db_post.id)
            ).all()
            post_aggregate.comments = [
                self.comment_mapper.to_domain(c) for c in comments
            ]

            files = self.session.exec(
                select(FileModel).where(FileModel.post_id == db_post.id)
            ).all()
            post_aggregate.files = [self.file_mapper.to_domain(f) for f in files]

            post_aggregates.append(post_aggregate)

        return post_aggregates
