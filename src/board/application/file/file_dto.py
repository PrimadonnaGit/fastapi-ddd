from pydantic import BaseModel


class FileCreateDTO(BaseModel):
    filename: str
    filepath: str
    post_id: int


class FileResponseDTO(BaseModel):
    id: int
    filename: str
    filepath: str
    post_id: int
