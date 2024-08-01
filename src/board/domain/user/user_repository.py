from abc import ABC, abstractmethod
from typing import Optional

from .user import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_nickname(self, nickname: str) -> Optional[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
