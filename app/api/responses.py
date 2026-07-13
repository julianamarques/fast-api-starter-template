from datetime import datetime, timezone
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field
from starlette import status
from starlette.responses import JSONResponse

from app.enums import ApiMessageEnum


T = TypeVar("T")


def _current_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


class ApiResponse(BaseModel, Generic[T]):
    status_code: int = status.HTTP_200_OK
    message: str = ApiMessageEnum.REQUEST_COMPLETED.value
    timestamp: str = Field(default_factory=_current_timestamp)
    content: Optional[T] = None


class ApiExceptionResponse(JSONResponse):
    def __init__(
            self,
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
            message: str = ApiMessageEnum.UNKNOWN_ERROR.value,
            *,
            path: str = "",
            body: Optional[Any] = None,
            headers: Optional[dict] = None
    ):
        data = {
            "status_code": status_code,
            "message": message,
            "timestamp": _current_timestamp(),
            "path": path,
            "body": body,
        }

        super().__init__(status_code=status_code, content=data, headers=headers)
