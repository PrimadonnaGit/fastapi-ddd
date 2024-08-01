from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostCreateDTO(BaseModel):
    title: str
    content: str
    is_admin_post: bool = False
    category_id: int
    tags: list[str] = []


class PostUpdateDTO(BaseModel):
    title: str
    content: str
    category_id: int
    tags: list[str] = []


class PostResponseDTO(BaseModel):
    id: int
    title: str
    content: str
    is_admin_post: bool
    views: int
    created_at: datetime
    updated_at: Optional[datetime]
    category_id: int
    user_id: int
    tags: list[str]
