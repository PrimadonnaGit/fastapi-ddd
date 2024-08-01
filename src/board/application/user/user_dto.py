from pydantic import BaseModel
from datetime import datetime


class UserRegisterDTO(BaseModel):
    user_id: str
    nickname: str
    password: str


class UserResponseDTO(BaseModel):
    id: int
    user_id: str
    nickname: str
    is_admin: bool
    create_time: datetime
    is_withdraw: bool
