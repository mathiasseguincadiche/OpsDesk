import os

os.environ.update(
    DATABASE_URL=os.environ.get("TEST_DATABASE_URL", "sqlite:///:memory:"),
    PASSWORD_HASH_ITERATIONS="1000",
    SEED_DEMO_DATA="false",
    ADMIN_EMAIL="admin@test.local",
    ADMIN_PASSWORD="AdminPass123",
    LOG_FORMAT="text",
    LOG_LEVEL="WARNING",
    JWT_SECRET="test-secret-test-secret-test-secret-42",
)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.db import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture()
def client():
    Base.metadata.drop_all(engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(engine)


def login(client, email, password):
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture()
def admin(client):
    return login(client, "admin@test.local", "AdminPass123")


@pytest.fixture()
def agent(client, admin):
    r = client.post("/api/users", headers=admin, json={"email": "agent@test.local", "full_name": "Agent Smith", "password": "AgentPass123", "role": "agent"})
    assert r.status_code == 201, r.text
    return login(client, "agent@test.local", "AgentPass123")


@pytest.fixture()
def user(client):
    r = client.post("/api/auth/register", json={"email": "user@test.local", "full_name": "Jane User", "password": "UserPass123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture()
def other_user(client):
    r = client.post("/api/auth/register", json={"email": "other@test.local", "full_name": "Other User", "password": "OtherPass123"})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}
