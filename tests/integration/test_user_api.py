from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    response = client.post(
        "/api/v1/users/register",
        json={
            "user_id": "testuser",
            "nickname": "Test User",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "testuser"
    assert data["nickname"] == "Test User"


def test_login(client: TestClient):
    # First, register a user
    client.post(
        "/api/v1/users/register",
        json={
            "user_id": "testuser",
            "nickname": "Test User",
            "password": "password123",
        },
    )

    # Then, try to login
    response = client.post(
        "/token", data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_update_user(client: TestClient):
    # Register a user
    register_response = client.post(
        "/api/v1/users/register",
        json={
            "user_id": "testuser",
            "nickname": "Test User",
            "password": "password123",
        },
    )
    user_id = register_response.json()["id"]

    # Login to get the token
    login_response = client.post(
        "/token", data={"username": "testuser", "password": "password123"}
    )
    token = login_response.json()["access_token"]

    # Update the user
    update_response = client.put(
        f"/api/v1/users/{user_id}",
        json={"nickname": "Updated User"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["nickname"] == "Updated User"
