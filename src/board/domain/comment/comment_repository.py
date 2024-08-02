from abc import ABC, abstractmethod

from .comment import Comment


class CommentRepository(ABC):
    @abstractmethod
    def save(self, comment: Comment) -> Comment:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Comment | None:
        pass

    @abstractmethod
    def find_by_post_id(self, post_id: int) -> list[Comment]:
        pass

    @abstractmethod
    def update(self, comment: Comment) -> Comment:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
