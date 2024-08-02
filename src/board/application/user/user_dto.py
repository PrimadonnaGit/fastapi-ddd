from datetime import datetime

from pydantic import BaseModel, model_validator


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

    class Config:
        from_attributes = True


class UserUpdateDTO(BaseModel):
    user_id: str | None = None
    nickname: str | None = None
    password: str | None = None

    @model_validator(mode="after")
    def check_at_least_one_field(self):
        if all(value is None for value in self.model_dump().values()):
            raise ValueError("At least one field must be provided for update")
        return self
