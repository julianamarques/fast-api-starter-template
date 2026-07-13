from datetime import datetime, timedelta, timezone

import jwt

from app.core.app_config import settings
from app.models.user import User
from tests.utils import API_PREFIX, create_user, login


def get_me(client, token: str):
    return client.get(f"{API_PREFIX}/auth/me", headers={"Authorization": f"Bearer {token}"})


def test_me_returns_authenticated_user(client):
    create_user(client)
    token = login(client).json()["content"]["access_token"]

    response = get_me(client, token)

    assert response.status_code == 200
    content = response.json()["content"]
    assert content["user_data"]["email"] == "julia@test.com"
    assert "password" not in content["user_data"]


def test_me_without_token_returns_401_with_www_authenticate_header(client):
    response = client.get(f"{API_PREFIX}/auth/me")

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_me_with_invalid_token_returns_401(client):
    response = get_me(client, "not-a-token")

    assert response.status_code == 401
    assert "Token invalido" in response.json()["body"]


def test_me_with_expired_token_returns_401(client):
    create_user(client)
    expired_token = jwt.encode(
        {"sub": "julia@test.com", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
        settings.SECRET_KEY,
        algorithm=settings.TOKEN_ALGORITHM,
    )

    response = get_me(client, expired_token)

    assert response.status_code == 401
    assert "Token expirado" in response.json()["body"]


def test_me_with_token_of_deleted_user_returns_401(client, db_session_factory):
    create_user(client)
    token = login(client).json()["content"]["access_token"]
    with db_session_factory() as session:
        session.query(User).delete()
        session.commit()

    response = get_me(client, token)

    assert response.status_code == 401
