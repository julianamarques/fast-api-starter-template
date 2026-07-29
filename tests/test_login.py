import time

from app.models.user import User
from app.utils import token_utils
from tests.utils import create_user, login


def test_login_normalizes_email_and_returns_token(client, db_session_factory):
    create_user(client, email="Juliana@Test.com")

    response = login(client, email="  JULIANA@test.com ")

    assert response.status_code == 200
    content = response.json()["content"]
    assert content["token_type"] == "bearer"
    assert content["user_data"]["email"] == "juliana@test.com"
    assert "password" not in content["user_data"]

    with db_session_factory() as session:
        user = session.query(User).filter_by(email="juliana@test.com").one()

    assert token_utils.decode(content["access_token"])["sub"] == str(user.id)


def test_login_failures_are_indistinguishable(client):
    create_user(client)

    wrong_password = login(client, password="senha-errada-1")
    start = time.perf_counter()
    unknown_email = login(client, email="ghost@test.com")
    elapsed = time.perf_counter() - start

    assert wrong_password.status_code == unknown_email.status_code == 401
    assert wrong_password.json()["message"] == unknown_email.json()["message"]
    assert wrong_password.json()["body"] == unknown_email.json()["body"]
    assert elapsed > 0.02


def test_inactive_user_login_is_indistinguishable_from_invalid(client, db_session_factory):
    create_user(client)

    with db_session_factory() as session:
        user = session.query(User).filter_by(email="juliana@test.com").one()
        user.active = False
        session.commit()

    inactive = login(client)
    wrong_password = login(client, password="senha-errada-1")

    assert inactive.status_code == wrong_password.status_code == 401
    assert inactive.json()["message"] == wrong_password.json()["message"]
    assert inactive.json()["body"] == wrong_password.json()["body"]
