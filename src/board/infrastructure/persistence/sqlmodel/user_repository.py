from typing import Optional

from sqlmodel import Session, select

from board.domain.user.user import User
from board.domain.user.user_repository import UserRepository
from board.infrastructure.persistence.mappers.sqlmodel.user_mapper import (
    SQLModelUserMapper,
)
from .models import UserModel


class SQLModelUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session
        self.mapper = SQLModelUserMapper()

    def save(self, user: User) -> User:
        db_user = self.mapper.to_orm(user)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return self.mapper.to_domain(db_user)

    def find_by_id(self, id: int) -> Optional[User]:
        statement = select(UserModel).where(UserModel.id == id)
        db_user = self.session.exec(statement).first()
        return self.mapper.to_domain(db_user) if db_user else None

    def find_by_user_id(self, user_id: str) -> Optional[User]:
        statement = select(UserModel).where(UserModel.user_id == user_id)
        db_user = self.session.exec(statement).first()
        return self.mapper.to_domain(db_user) if db_user else None

    def find_by_nickname(self, nickname: str) -> Optional[User]:
        statement = select(UserModel).where(UserModel.nickname == nickname)
        db_user = self.session.exec(statement).first()
        return self.mapper.to_domain(db_user) if db_user else None

    def update(self, user: User) -> User:
        db_user = self.session.get(UserModel, user.id)
        if db_user:
            updated_db_user = self.mapper.to_orm(user)
            for key, value in updated_db_user.__dict__.items():
                setattr(db_user, key, value)
            self.session.add(db_user)
            self.session.commit()
            self.session.refresh(db_user)
        return self.mapper.to_domain(db_user)

    def delete(self, id: int) -> None:
        db_user = self.session.get(UserModel, id)
        if db_user:
            self.session.delete(db_user)
            self.session.commit()
