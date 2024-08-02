from board.domain.shared.value_objects import Password
from board.domain.user.user import User
from board.domain.user.user_repository import UserRepository
from .user_dto import UserRegisterDTO, UserResponseDTO, UserUpdateDTO


class UserApplicationService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, user_dto: UserRegisterDTO) -> UserResponseDTO:
        if self.user_repository.find_by_user_id(user_dto.user_id):
            raise ValueError("User ID already exists")
        if self.user_repository.find_by_nickname(user_dto.nickname):
            raise ValueError("Nickname already exists")

        password = Password(value=user_dto.password)
        user = User(
            user_id=user_dto.user_id,
            nickname=user_dto.nickname,
            password=password.hashed_value,
            is_admin=False,
            is_withdraw=False,
        )
        saved_user = self.user_repository.save(user)

        return UserResponseDTO.model_validate(saved_user)

    def get_user_by_id(self, user_id: int) -> UserResponseDTO | None:
        user = self.user_repository.find_by_id(user_id)
        return UserResponseDTO.model_validate(user) if user else None

    def update_user(
        self, user_id: int, user_update_dto: UserUpdateDTO
    ) -> UserResponseDTO:
        existing_user = self.user_repository.find_by_id(user_id)
        if not existing_user:
            raise ValueError("User not found")

        if user_update_dto.user_id is not None:
            if (
                existing_user.user_id != user_update_dto.user_id
                and self.user_repository.find_by_user_id(user_update_dto.user_id)
            ):
                raise ValueError("User ID already exists")
            existing_user.user_id = user_update_dto.user_id

        if user_update_dto.nickname is not None:
            if (
                existing_user.nickname != user_update_dto.nickname
                and self.user_repository.find_by_nickname(user_update_dto.nickname)
            ):
                raise ValueError("Nickname already exists")
            existing_user.nickname = user_update_dto.nickname

        if user_update_dto.password is not None:
            password = Password(value=user_update_dto.password)
            existing_user.password = password.hashed_value

        updated_user = self.user_repository.update(existing_user)
        return UserResponseDTO.model_validate(updated_user)

    def delete_user(self, user_id: int) -> None:
        self.user_repository.delete(user_id)
