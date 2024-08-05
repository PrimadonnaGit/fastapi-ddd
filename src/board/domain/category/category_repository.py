from abc import ABC, abstractmethod

from .category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category) -> Category:
        pass

    @abstractmethod
    def find_by_id(self, category_id: int) -> Category | None:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Category | None:
        pass

    @abstractmethod
    def find_all(self) -> list[Category]:
        pass

    @abstractmethod
    def update(self, category: Category) -> Category:
        pass

    @abstractmethod
    def delete(self, category_id: int) -> None:
        pass
