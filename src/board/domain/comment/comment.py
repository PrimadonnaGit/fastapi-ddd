from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Comment(BaseModel):
    id: Optional[int] = None
    content: str
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
    post_id: int
    user_id: int
    parent_comment_id: Optional[int] = None
