from passlib.context import CryptContext
from pydantic import BaseModel, field_validator

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Password(BaseModel):
    value: str

    @field_validator("value")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

    @property
    def hashed_value(self):
        return pwd_context.hash(self.value)

    def verify(self, plain_password):
        return pwd_context.verify(plain_password, self.value)
