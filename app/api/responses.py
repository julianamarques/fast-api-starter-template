from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse

from app.enums import ApiMessageEnum


class ApiResponse(BaseModel):
    status_code: int = status.HTTP_200_OK
    message: str = ApiMessageEnum.REQUEST_COMPLETED.value
    timestamp: str = datetime.now().isoformat()
    content: Optional[Any] = None


class ApiExceptionResponse(JSONResponse):
    def __init__(
            self,
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
            message: str = ApiMessageEnum.UNKNOWN_ERROR.value,
            *,
            timestamp: str = datetime.now().isoformat(),
            path: str = "",
            body: Optional[Any] = None
    ):
        data = {
            "status_code": status_code,
            "message": message,
            "timestamp": timestamp,
            "path": path,
            "body": body,
        }

        super().__init__(status_code=status_code, content=data)
