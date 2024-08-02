from pydantic import BaseModel


class FileDTO(BaseModel):
    id: int
    filename: str
    filepath: str


class FileCreateDTO(BaseModel):
    filename: str
    filepath: str
    post_id: int


class FileResponseDTO(BaseModel):
    id: int
    filename: str
    filepath: str
    post_id: int
