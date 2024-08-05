from abc import ABC, abstractmethod

from .post_aggregate import PostAggregate


class PostRepository(ABC):
    @abstractmethod
    def save(self, post_aggregate: PostAggregate) -> PostAggregate:
        pass

    @abstractmethod
    def find_by_id(self, post_id: int) -> PostAggregate | None:
        pass

    @abstractmethod
    def delete(self, post_id: int) -> None:
        pass

    @abstractmethod
    def update(self, post_aggregate: PostAggregate) -> PostAggregate:
        pass

    @abstractmethod
    def search(self, query: str, limit: int, offset: int) -> list[PostAggregate]:
        pass
