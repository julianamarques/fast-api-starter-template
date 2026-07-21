from app.core.app_config import Settings
from tests.utils import API_PREFIX


def test_docs_urls_are_disabled_in_production():
    prod = Settings(ENVIRONMENT="production")

    assert prod.is_production is True
    assert prod.openapi_url is None
    assert prod.docs_url is None
    assert prod.redoc_url is None


def test_docs_urls_are_enabled_outside_production():
    for environment in ("development", "testing"):
        settings = Settings(ENVIRONMENT=environment)

        assert settings.is_production is False
        assert settings.docs_url == "/docs"
        assert settings.redoc_url == "/redoc"
        assert settings.openapi_url == f"{settings.API_PREFIX}/openapi.json"


def test_docs_endpoints_are_served_in_test_environment(client):
    assert client.get("/docs").status_code == 200
    assert client.get("/redoc").status_code == 200
    assert client.get(f"{API_PREFIX}/openapi.json").status_code == 200
