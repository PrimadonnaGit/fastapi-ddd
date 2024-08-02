from datetime import datetime

from .user import User
from .user_repository import UserRepository
from ..shared.value_objects import Password


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, user_id: str, nickname: str, password: str) -> User:
        if self.user_repository.find_by_user_id(user_id):
            raise ValueError("User ID already exists")
        if self.user_repository.find_by_nickname(nickname):
            raise ValueError("Nickname already exists")

        hashed_password = Password(value=password).hashed_value
        user = User(
            id=None,
            user_id=user_id,
            nickname=nickname,
            password=hashed_password,
            is_admin=False,
            create_time=datetime.utcnow(),
            is_withdraw=False,
        )
        return self.user_repository.save(user)
