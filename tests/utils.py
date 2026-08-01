from fastapi.testclient import TestClient
from httpx2 import Response

from app.core.app_config import settings

API_PREFIX = settings.API_PREFIX
DEFAULT_EMAIL = "juliana@test.com"
DEFAULT_PASSWORD = "senha-123456"


def user_payload(**overrides) -> dict:
    payload = {
        "name": "Juliana Marques",
        "email": DEFAULT_EMAIL,
        "password": DEFAULT_PASSWORD,
        "confirm_password": DEFAULT_PASSWORD,
    }
    payload.update(overrides)

    return payload


def create_user(client: TestClient, **overrides) -> Response:
    return client.post(f"{API_PREFIX}/auth/create-user", json=user_payload(**overrides))


def login(client: TestClient, email: str = DEFAULT_EMAIL, password: str = DEFAULT_PASSWORD) -> Response:
    return client.post(
        f"{API_PREFIX}/auth/login",
        data={"username": email, "password": password},
    )
