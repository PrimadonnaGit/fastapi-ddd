from datetime import datetime

from pydantic import BaseModel


class Post(BaseModel):
    id: int | None = None
    title: str
    content: str
    is_admin_post: bool = False
    views: int = 0
    created_at: datetime = datetime.utcnow()
    updated_at: datetime | None = None
    category_id: int
    user_id: int
    tags: list[str] = []
