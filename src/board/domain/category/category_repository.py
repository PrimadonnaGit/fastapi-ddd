from abc import ABC, abstractmethod
from typing import Optional

from .category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category) -> Category:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Category]:
        pass

    @abstractmethod
    def find_all(self) -> list[Category]:
        pass

    @abstractmethod
    def update(self, category: Category) -> Category:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
