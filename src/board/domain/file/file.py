from pydantic import BaseModel


class File(BaseModel):
    id: int | None = None
    filename: str
    filepath: str
    post_id: int
