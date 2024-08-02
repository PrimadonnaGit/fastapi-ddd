from abc import ABC, abstractmethod

from .file import File


class FileRepository(ABC):
    @abstractmethod
    def save(self, file: File) -> File:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> File | None:
        pass

    @abstractmethod
    def find_by_post_id(self, post_id: int) -> list[File]:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
