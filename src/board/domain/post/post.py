from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    is_admin_post: bool = False
    views: int = 0
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
    category_id: int
    user_id: int
    tags: list[str] = []
