from pydantic import BaseModel


class Category(BaseModel):
    id: int | None = None
    name: str
