import asyncio
import time
from datetime import datetime, timezone

from starlette.requests import Request

from app.api.responses import ApiResponse
from app.core.app_config import settings
from app.handlers import internal_server_error_exception_handler
from app.utils import token_utils


def test_token_expiration_is_utc():
    token_data = token_utils.encode(username="tz@test.com")

    decoded_exp = token_utils.decode(token_data["access_token"])["exp"]
    expected_exp = datetime.now(timezone.utc).timestamp() + settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

    assert abs(decoded_exp - expected_exp) < 60
    assert datetime.fromisoformat(token_data["expires_in"]).utcoffset() is not None


def test_api_response_timestamp_is_generated_per_response():
    first = ApiResponse()
    time.sleep(0.001)
    second = ApiResponse()

    assert first.timestamp.endswith("+00:00")
    assert first.timestamp != second.timestamp


def test_internal_error_response_hides_exception_details():
    scope = {
        "type": "http", "method": "GET", "scheme": "http", "server": ("test", 80),
        "path": "/route", "raw_path": b"/route", "query_string": b"",
        "headers": [], "root_path": "",
    }

    response = asyncio.run(
        internal_server_error_exception_handler(Request(scope), RuntimeError("internal-secret"))
    )

    assert response.status_code == 500
    assert b"internal-secret" not in response.body
