from datetime import datetime

from pydantic import BaseModel

from board.application.comment.comment_dto import CommentDTO
from board.application.file.file_dto import FileDTO
from board.domain.post.post_aggregate import PostAggregate


class PostCreateDTO(BaseModel):
    title: str
    content: str
    category_id: int

    @classmethod
    def from_aggregate(cls, aggregate: "PostAggregate"):
        return cls(
            title=aggregate.post.title,
            content=aggregate.post.content,
            category_id=aggregate.post.category_id,
        )


class PostUpdateDTO(BaseModel):
    title: str
    content: str
    category_id: int

    @classmethod
    def from_aggregate(cls, aggregate: "PostAggregate"):
        return cls(
            title=aggregate.post.title,
            content=aggregate.post.content,
            category_id=aggregate.post.category_id,
        )


class PostResponseDTO(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    category_id: int
    created_at: datetime
    updated_at: datetime | None
    comments: list[CommentDTO]
    files: list[FileDTO]

    @classmethod
    def from_aggregate(cls, aggregate: "PostAggregate"):
        return cls(
            id=aggregate.post.id,
            title=aggregate.post.title,
            content=aggregate.post.content,
            user_id=aggregate.post.user_id,
            category_id=aggregate.post.category_id,
            created_at=aggregate.post.created_at,
            updated_at=aggregate.post.updated_at,
            comments=[
                CommentDTO(
                    id=comment.id,
                    content=comment.content,
                    user_id=comment.user_id,
                    created_at=comment.created_at,
                )
                for comment in aggregate.comments
            ],
            files=[
                FileDTO(id=file.id, filename=file.filename, filepath=file.filepath)
                for file in aggregate.files
            ],
        )


class PostSearchDTO(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    category_id: int
    created_at: datetime
    updated_at: datetime | None
    comment_count: int
    file_count: int

    @classmethod
    def from_aggregate(cls, aggregate: "PostAggregate"):
        return cls(
            id=aggregate.post.id,
            title=aggregate.post.title,
            content=(
                aggregate.post.content[:200] + "..."
                if len(aggregate.post.content) > 200
                else aggregate.post.content
            ),
            user_id=aggregate.post.user_id,
            category_id=aggregate.post.category_id,
            created_at=aggregate.post.created_at,
            updated_at=aggregate.post.updated_at,
            comment_count=len(aggregate.comments),
            file_count=len(aggregate.files),
        )
