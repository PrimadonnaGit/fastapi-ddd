from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    response = client.post(
        "/api/v1/users/register",
        json={
            "user_id": "newuser",
            "nickname": "New User",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "newuser"
    assert data["nickname"] == "New User"


def test_login(client: TestClient):
    # First, register a user
    client.post(
        "/api/v1/users/register",
        json={
            "user_id": "loginuser",
            "nickname": "Login User",
            "password": "password123",
        },
    )

    # Then, try to login
    response = client.post(
        "/token", data={"username": "loginuser", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_create_post(client: TestClient, login_user):
    response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post", "content": "This is a test post", "category_id": 1},
        headers=login_user,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test post"
    return data["id"]


def test_get_post(client: TestClient, login_user):
    post_id = test_create_post(client, login_user)
    response = client.get(f"/api/v1/posts/{post_id}", headers=login_user)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test post"


def test_update_post(client: TestClient, login_user):
    post_id = test_create_post(client, login_user)
    response = client.put(
        f"/api/v1/posts/{post_id}",
        json={"title": "Updated Test Post", "content": "This is an updated test post"},
        headers=login_user,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Test Post"
    assert data["content"] == "This is an updated test post"


def test_search_posts(client: TestClient, login_user):
    test_create_post(client, login_user)
    response = client.get("/api/v1/posts/search?query=Test", headers=login_user)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(post["title"] == "Test Post" for post in data)


def test_delete_post(client: TestClient, login_user):
    post_id = test_create_post(client, login_user)
    response = client.delete(f"/api/v1/posts/{post_id}", headers=login_user)
    assert response.status_code == 200
    assert response.json() == {"message": "Post deleted successfully"}

    # Verify the post is deleted
    response = client.get(f"/api/v1/posts/{post_id}", headers=login_user)
    assert response.status_code == 404
