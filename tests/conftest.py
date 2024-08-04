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
