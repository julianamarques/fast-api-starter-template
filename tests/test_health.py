from tests.utils import API_PREFIX


def test_health_check(client):
    response = client.get(f"{API_PREFIX}/health/check")

    assert response.status_code == 200
    body = response.json()
    assert body["status_code"] == 200
    assert body["message"] == "Requisição concluída"
    assert body["content"] == "Up!"


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
