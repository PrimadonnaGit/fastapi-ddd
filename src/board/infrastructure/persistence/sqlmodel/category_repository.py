from typing import Optional

from sqlmodel import Session, select

from board.domain.category.category import Category
from board.domain.category.category_repository import CategoryRepository
from board.infrastructure.persistence.mappers.sqlmodel.category_mapper import (
    SQLModelCategoryMapper,
)
from .models import CategoryModel


class SQLModelCategoryRepository(CategoryRepository):
    def __init__(self, session: Session):
        self.session = session
        self.mapper = SQLModelCategoryMapper()

    def save(self, category: Category) -> Category:
        db_category = self.mapper.to_orm(category)
        self.session.add(db_category)
        self.session.commit()
        self.session.refresh(db_category)
        return self.mapper.to_domain(db_category)

    def find_by_id(self, id: int) -> Optional[Category]:
        statement = select(CategoryModel).where(CategoryModel.id == id)
        db_category = self.session.exec(statement).first()
        return self.mapper.to_domain(db_category) if db_category else None

    def find_all(self) -> list[Category]:
        statement = select(CategoryModel)
        db_categories = self.session.exec(statement).all()
        return [self.mapper.to_domain(db_category) for db_category in db_categories]

    def update(self, category: Category) -> Category:
        db_category = self.session.get(CategoryModel, category.id)
        if db_category:
            db_category.name = category.name
            self.session.add(db_category)
            self.session.commit()
            self.session.refresh(db_category)
        return self.mapper.to_domain(db_category)

    def delete(self, id: int) -> None:
        db_category = self.session.get(CategoryModel, id)
        if db_category:
            self.session.delete(db_category)
            self.session.commit()
