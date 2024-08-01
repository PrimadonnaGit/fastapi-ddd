from board.domain.category.category import Category
from board.domain.category.category_repository import CategoryRepository
from .category_dto import CategoryCreateDTO, CategoryResponseDTO


class CategoryApplicationService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def create_category(self, category_dto: CategoryCreateDTO) -> CategoryResponseDTO:
        category = Category(name=category_dto.name)
        saved_category = self.category_repository.save(category)
        return CategoryResponseDTO.model_validate(saved_category)

    def get_all_categories(self) -> list[CategoryResponseDTO]:
        categories = self.category_repository.find_all()
        return [CategoryResponseDTO.model_validate(category) for category in categories]

    def update_category(
            self, id: int, category_dto: CategoryCreateDTO
    ) -> CategoryResponseDTO:
        category = self.category_repository.find_by_id(id)
        if not category:
            raise ValueError("Category not found")
        category.name = category_dto.name
        updated_category = self.category_repository.update(category)
        return CategoryResponseDTO.model_validate(updated_category)

    def delete_category(self, id: int) -> None:
        self.category_repository.delete(id)
