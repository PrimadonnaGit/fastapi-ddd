from abc import ABC, abstractmethod
from typing import Optional

from .post import Post


class PostRepository(ABC):
    @abstractmethod
    def save(self, post: Post) -> Post:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Post]:
        pass

    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100) -> list[Post]:
        pass

    @abstractmethod
    def update(self, post: Post) -> Post:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass

    @abstractmethod
    def search(self, query: str) -> list[Post]:
        pass
