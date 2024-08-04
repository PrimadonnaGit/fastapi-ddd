from src.board.domain.user.user import User


def test_user_creation():
    user = User(
        id=1,
        user_id="testuser",
        nickname="Test User",
        password="hashed_password",
        is_admin=False,
        is_withdraw=False,
    )
    assert user.id == 1
    assert user.user_id == "testuser"
    assert user.nickname == "Test User"
    assert user.password == "hashed_password"
    assert user.is_admin is False
    assert user.is_withdraw is False


def test_user_withdraw():
    user = User(
        id=1,
        user_id="testuser",
        nickname="Test User",
        password="hashed_password",
        is_admin=False,
        is_withdraw=False,
    )
    user.withdraw()
    assert user.is_withdraw == True
