import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from src.main import create_app


@pytest.fixture(scope="function")
def client():
    app = create_app()
    with TestClient(app) as client:
        yield client

    SQLModel.metadata.drop_all(app.container.db_engine())


@pytest.fixture(scope="function")
def login_user(client: TestClient):
    client.post(
        "/api/v1/users/register",
        json={
            "user_id": "testuser",
            "nickname": "Test User",
            "password": "password123",
        },
    )

    response = client.post(
        "/token", data={"username": "testuser", "password": "password123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
