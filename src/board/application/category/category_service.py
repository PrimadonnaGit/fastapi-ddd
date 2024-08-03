from board.domain.category.category import Category
from board.domain.category.category_repository import CategoryRepository
from .category_dto import CategoryCreateDTO, CategoryResponseDTO, CategoryUpdateDTO


class CategoryApplicationService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def create_category(
        self, category_create_dto: CategoryCreateDTO
    ) -> CategoryResponseDTO:
        if self.category_repository.find_by_name(category_create_dto.name):
            raise ValueError("Category already exists")

        category = Category(name=category_create_dto.name)
        saved_category = self.category_repository.save(category)
        return CategoryResponseDTO.model_validate(saved_category)

    def get_all_categories(self) -> list[CategoryResponseDTO]:
        categories = self.category_repository.find_all()
        return [CategoryResponseDTO.model_validate(category) for category in categories]

    def update_category(
        self, category_id: int, category_update_dto: CategoryUpdateDTO
    ) -> CategoryResponseDTO:
        existing_category = self.category_repository.find_by_id(category_id)
        if not existing_category:
            raise ValueError("Category not found")

        if (
            category_update_dto.name is not None
            and self.category_repository.find_by_name(category_update_dto.name)
        ):
            raise ValueError("Category already exists")

        existing_category.name = category_update_dto.name
        updated_category = self.category_repository.update(existing_category)
        return CategoryResponseDTO.model_validate(updated_category)

    def delete_category(self, id: int) -> None:
        self.category_repository.delete(id)
