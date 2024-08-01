from pydantic import BaseModel


class CategoryCreateDTO(BaseModel):
    name: str


class CategoryResponseDTO(BaseModel):
    id: int
    name: str
