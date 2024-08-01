from typing import Optional

from pydantic import BaseModel


class File(BaseModel):
    id: Optional[int] = None
    filename: str
    filepath: str
    post_id: int
