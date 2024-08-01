from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CommentCreateDTO(BaseModel):
    content: str
    post_id: int
    parent_comment_id: Optional[int] = None


class CommentUpdateDTO(BaseModel):
    content: str


class CommentResponseDTO(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: Optional[datetime]
    post_id: int
    user_id: int
    parent_comment_id: Optional[int]
