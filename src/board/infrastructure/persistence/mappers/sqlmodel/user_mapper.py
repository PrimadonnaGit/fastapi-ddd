from board.domain.user.user import User
from board.infrastructure.persistence.mappers.base import BaseMapper
from board.infrastructure.persistence.sqlmodel.models import UserModel


class SQLModelUserMapper(BaseMapper[User, UserModel]):
    @staticmethod
    def to_domain(db_user: UserModel) -> User:
        return User(
            id=db_user.id,
            user_id=db_user.user_id,
            nickname=db_user.nickname,
            password=db_user.password,
            is_admin=db_user.is_admin,
            create_time=db_user.create_time,
            is_withdraw=db_user.is_withdraw,
        )

    @staticmethod
    def to_orm(user: User) -> UserModel:
        return UserModel(
            id=user.id,
            user_id=user.user_id,
            nickname=user.nickname,
            password=user.password,
            is_admin=user.is_admin,
            create_time=user.create_time,
            is_withdraw=user.is_withdraw,
        )
