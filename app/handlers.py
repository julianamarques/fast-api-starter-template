import logging
from typing import Union

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.exceptions import HTTPException

from app.api.responses import ApiExceptionResponse
from app.enums import ApiMessageEnum


log = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exception: Union[HTTPException, Exception]) -> ApiExceptionResponse:
    if exception.status_code == status.HTTP_404_NOT_FOUND:
        log.error(f"Route {request.url.path} not found!", exc_info=exception)

        return ApiExceptionResponse(
            status_code=exception.status_code,
            message=ApiMessageEnum.ROUTE_NOT_FOUND.value,
            path=request.url.path
        )
    elif exception.status_code == status.HTTP_400_BAD_REQUEST:
        log.error(f"Invalid request for route {request.url.path}", exc_info=exception)

        return ApiExceptionResponse(
            status_code=exception.status_code,
            message=ApiMessageEnum.INVALID_REQUEST.value,
            path=request.url.path,
            content=[exception.detail]
        )
    elif exception.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
        log.error(f"Method {request.method} not allowed for route {request.url.path}", exc_info=exception)

        return ApiExceptionResponse(
            status_code=exception.status_code,
            message=ApiMessageEnum.NOT_ALLOWED_METHOD.value,
            path=request.url.path,
            content=[f"Method {request.method} not allowed for route"]
        )
    elif exception.status_code == status.HTTP_401_UNAUTHORIZED:
        log.error(f"Access Denied for route {request.url.path}", exc_info=exception)

        return ApiExceptionResponse(
            status_code=exception.status_code,
            message=ApiMessageEnum.ACCESS_DENIED.value,
            path=request.url.path,
            content=[exception.detail]
        )
    elif exception.status_code == status.HTTP_401_UNAUTHORIZED:
        log.error(f"Unauthorized access for route {request.url.path}", exc_info=exception)

        return ApiExceptionResponse(
            status_code=exception.status_code,
            message=ApiMessageEnum.ACCESS_DENIED.value,
            path=request.url.path,
            content=[exception.detail]
        )

    return ApiExceptionResponse(
        status_code=exception.status_code,
        path=request.url.path,
        message=exception.detail,
    )


async def validation_exception_handler(request: Request, exception: Union[RequestValidationError, Exception]) -> ApiExceptionResponse:
    errors = []

    for error in exception.errors():
        loc = " -> ".join(map(str, error["loc"]))
        msg = error["msg"]
        errors.append(f"{loc}: {msg}")

    log.error(f"Route: {request.url.path}", exc_info=exception)
    log.error(f"Validation Error: {errors}", exc_info=exception)

    content = f"Invalid arguments [{errors}]"

    return ApiExceptionResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message=ApiMessageEnum.INVALID_ARGUMENT.value,
        path=request.url.path,
        content=content
    )


async def internal_server_error_exeption_handler(request: Request, exception: Exception) -> ApiExceptionResponse:
    log.error(f"Internal Server Error for route: {request.url.path}", exc_info=exception)

    return ApiExceptionResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=ApiMessageEnum.UNKNOWN_ERROR.value,
        path=request.url.path,
        content=[str(exception)]
    )
