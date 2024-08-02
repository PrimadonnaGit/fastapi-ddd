from datetime import datetime

from pydantic import BaseModel


class Comment(BaseModel):
    id: int | None = None
    content: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime | None = None
    post_id: int
    user_id: int
    parent_comment_id: int | None = None
