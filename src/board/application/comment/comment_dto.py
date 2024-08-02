from datetime import datetime

from pydantic import BaseModel


class CommentDTO(BaseModel):
    id: int
    content: str
    user_id: int
    created_at: datetime


class CommentCreateDTO(BaseModel):
    content: str
    post_id: int
    parent_comment_id: int | None = None


class CommentUpdateDTO(BaseModel):
    content: str


class CommentResponseDTO(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime | None
    post_id: int
    user_id: int
    parent_comment_id: int | None
