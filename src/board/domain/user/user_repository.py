from abc import ABC, abstractmethod

from .user import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> User | None:
        pass

    @abstractmethod
    def find_by_nickname(self, nickname: str) -> User | None:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass
