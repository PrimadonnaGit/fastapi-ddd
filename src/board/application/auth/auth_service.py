from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from board.domain.shared.value_objects import Password
from board.domain.user.user_repository import UserRepository
from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthApplicationService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate_user(self, user_id: str, password: str):
        user = self.user_repository.find_by_user_id(user_id)
        if not user:
            return False
        if not Password(value=user.password).verify(password):
            return False

        return user

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt
