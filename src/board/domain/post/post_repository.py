from abc import ABC, abstractmethod

from .post_aggregate import PostAggregate


class PostRepository(ABC):
    @abstractmethod
    def save(self, post_aggregate: PostAggregate) -> PostAggregate:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> PostAggregate | None:
        pass

    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100) -> list[PostAggregate]:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass

    @abstractmethod
    def search(self, query: str) -> list[PostAggregate]:
        pass
