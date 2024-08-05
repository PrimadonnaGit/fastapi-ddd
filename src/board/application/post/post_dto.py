from datetime import datetime

from pydantic import BaseModel, model_validator

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
    title: str | None = None
    content: str | None = None
    category_id: int | None = None

    @classmethod
    def from_aggregate(cls, aggregate: "PostAggregate"):
        return cls(
            title=aggregate.post.title,
            content=aggregate.post.content,
            category_id=aggregate.post.category_id,
        )

    @model_validator(mode="after")
    def check_at_least_one_field(self):
        if all(value is None for value in self.model_dump().values()):
            raise ValueError("At least one field must be provided for update")
        return self


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

    class Config:
        from_attribute = True


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
    comments: list[CommentDTO]
    files: list[FileDTO]

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
