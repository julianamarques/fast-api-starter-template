from sqlalchemy.exc import SQLAlchemyError

from app.depends import get_db_session
from app.main import app
from tests.utils import API_PREFIX


def test_health_check(client):
    response = client.get(f"{API_PREFIX}/health/check")

    assert response.status_code == 200
    body = response.json()
    assert body["status_code"] == 200
    assert body["message"] == "Requisição concluída"
    assert body["content"] == "Up!"


def test_readiness_check_returns_ready_when_database_is_reachable(client):
    response = client.get(f"{API_PREFIX}/health/ready")

    assert response.status_code == 200
    body = response.json()
    assert body["status_code"] == 200
    assert body["content"] == "Ready!"


def test_readiness_check_returns_503_when_database_is_unreachable(client):
    def unavailable_db():
        class _Unavailable:
            def execute(self, *_args, **_kwargs):
                raise SQLAlchemyError("database is down")

        yield _Unavailable()

    app.dependency_overrides[get_db_session] = unavailable_db

    response = client.get(f"{API_PREFIX}/health/ready")

    assert response.status_code == 503
    assert response.json()["message"] == "Serviço externo indisponível"


def test_unknown_route_returns_standard_404(client):
    response = client.get(f"{API_PREFIX}/does-not-exist")

    assert response.status_code == 404
    body = response.json()
    assert body["message"] == "Rota não encontrada"
    assert body["path"] == f"{API_PREFIX}/does-not-exist"


def test_wrong_method_returns_standard_405(client):
    response = client.post(f"{API_PREFIX}/health/check")

    assert response.status_code == 405
    assert response.json()["message"] == "Método não permitido"
