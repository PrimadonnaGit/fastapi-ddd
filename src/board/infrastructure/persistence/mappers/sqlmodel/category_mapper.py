from board.domain.category.category import Category
from board.infrastructure.persistence.mappers.base import BaseMapper
from board.infrastructure.persistence.sqlmodel.models import CategoryModel


class SQLModelCategoryMapper(BaseMapper[Category, CategoryModel]):
    @staticmethod
    def to_domain(db_category: CategoryModel) -> Category:
        return Category(id=db_category.id, name=db_category.name)

    @staticmethod
    def to_orm(category: Category) -> CategoryModel:
        return CategoryModel(id=category.id, name=category.name)
