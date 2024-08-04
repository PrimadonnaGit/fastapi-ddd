import pytest

from board.application.user.user_dto import (
    UserRegisterDTO,
    UserUpdateDTO,
    UserResponseDTO,
)
from board.application.user.user_service import UserApplicationService


class MockUserRepository:
    def __init__(self):
        self.users = {}
        self.next_id = 1

    def save(self, user):
        if user.id is None:
            user.id = self.next_id
            self.next_id += 1
        self.users[user.id] = user
        return user

    def find_by_id(self, id):
        return self.users.get(id)

    def find_by_user_id(self, user_id):
        return next(
            (user for user in self.users.values() if user.user_id == user_id), None
        )

    def find_by_nickname(self, nickname):
        return next(
            (user for user in self.users.values() if user.nickname == nickname), None
        )

    def update(self, user):
        self.users[user.id] = user
        return user

    def delete(self, id):
        del self.users[id]


@pytest.fixture
def user_service():
    return UserApplicationService(MockUserRepository())


def test_register_user(user_service):
    dto = UserRegisterDTO(
        user_id="testuser", nickname="Test User", password="password123"
    )
    response = user_service.register_user(dto)
    assert isinstance(response, UserResponseDTO)
    assert response.id is not None
    assert response.user_id == "testuser"
    assert response.nickname == "Test User"


def test_register_user_duplicate_user_id(user_service):
    dto1 = UserRegisterDTO(
        user_id="testuser", nickname="Test User 1", password="password123"
    )
    user_service.register_user(dto1)

    dto2 = UserRegisterDTO(
        user_id="testuser", nickname="Test User 2", password="password456"
    )
    with pytest.raises(ValueError, match="User ID already exists"):
        user_service.register_user(dto2)


def test_update_user(user_service):
    register_dto = UserRegisterDTO(
        user_id="testuser", nickname="Test User", password="password123"
    )
    registered_user = user_service.register_user(register_dto)

    update_dto = UserUpdateDTO(nickname="Updated User")
    updated_user = user_service.update_user(registered_user.id, update_dto)
    assert updated_user.nickname == "Updated User"


def test_update_user_duplicate_user_id(user_service):
    dto1 = UserRegisterDTO(
        user_id="testuser1", nickname="Test User 1", password="password123"
    )
    user1 = user_service.register_user(dto1)

    dto2 = UserRegisterDTO(
        user_id="testuser2", nickname="Test User 2", password="password456"
    )
    user2 = user_service.register_user(dto2)

    update_dto = UserUpdateDTO(user_id="testuser2")
    with pytest.raises(ValueError, match="User ID already exists"):
        user_service.update_user(user1.id, update_dto)


def test_update_user_duplicate_nickname(user_service):
    dto1 = UserRegisterDTO(
        user_id="testuser1", nickname="Test User 1", password="password123"
    )
    user1 = user_service.register_user(dto1)

    dto2 = UserRegisterDTO(
        user_id="testuser2", nickname="Test User 2", password="password456"
    )
    user2 = user_service.register_user(dto2)

    update_dto = UserUpdateDTO(nickname="Test User 2")
    with pytest.raises(ValueError, match="Nickname already exists"):
        user_service.update_user(user1.id, update_dto)


def test_update_user_not_found(user_service):
    update_dto = UserUpdateDTO(nickname="Updated User")
    with pytest.raises(ValueError, match="User not found"):
        user_service.update_user(1, update_dto)


def test_delete_user(user_service):
    dto = UserRegisterDTO(
        user_id="testuser", nickname="Test User", password="password123"
    )
    user = user_service.register_user(dto)

    user_service.delete_user(user.id)
    assert user_service.get_user_by_id(user.id) is None
