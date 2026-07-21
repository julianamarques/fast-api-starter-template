from tests.utils import create_user


def test_create_user_returns_201_without_password(client):
    response = create_user(client, name="  Juliana  ", email="Nova@Test.com")

    assert response.status_code == 201
    body = response.json()
    assert body["status_code"] == 201
    content = body["content"]
    assert content["name"] == "Juliana"
    assert content["email"] == "nova@test.com"
    assert content["active"] is True
    assert content["admin"] is False
    assert "password" not in content


def test_create_user_with_duplicated_email_returns_400(client):
    create_user(client)

    response = create_user(client)

    assert response.status_code == 400
    assert "Já existe um usuário com esse email" in response.json()["body"]


def test_create_user_duplicated_email_race_falls_back_to_integrity_error(client, monkeypatch):
    create_user(client)
    monkeypatch.setattr(
        "app.services.user_service.UserService.find_user_by_email",
        lambda self, email: None,
    )

    response = create_user(client)

    assert response.status_code == 400
    assert "Já existe um usuário com esse email" in response.json()["body"]


def test_create_user_with_mismatched_passwords_returns_400(client):
    response = create_user(client, confirm_password="outra-senha-123")

    assert response.status_code == 400
    assert "As senhas não coincidem" in response.json()["body"]


def test_create_user_with_invalid_email_returns_422(client):
    response = create_user(client, email="not-an-email")

    assert response.status_code == 422
    assert response.json()["message"] == "Argumento inválido"


def test_create_user_with_short_password_returns_422(client):
    response = create_user(client, password="curta12", confirm_password="curta12")

    assert response.status_code == 422


def test_create_user_with_password_over_72_bytes_returns_422(client):
    multibyte_password = "ç" * 40  # 40 caracteres, 80 bytes em UTF-8

    response = create_user(client, password=multibyte_password, confirm_password=multibyte_password)

    assert response.status_code == 422
