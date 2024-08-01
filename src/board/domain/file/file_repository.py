from abc import ABC, abstractmethod
from typing import Optional

from .file import File


class FileRepository(ABC):
    @abstractmethod
    def save(self, file: File) -> File:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[File]:
        pass

    @abstractmethod
    def find_by_post_id(self, post_id: int) -> list[File]:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
