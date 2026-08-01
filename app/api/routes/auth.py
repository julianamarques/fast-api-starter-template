from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.responses import ApiResponse
from app.core.database_config import Session
from app.depends import get_db_session, get_auth_user as auth_user
from app.schemas.auth_schema import (
    AuthUserResponseSchema,
    LoginRequestSchema,
    UserCreateRequestSchema
)
from app.schemas.user_schema import UserResponseSchema
from app.services.auth_service import AuthService
from app.services.user_service import UserService


router = APIRouter()


@router.post("/login", response_model=ApiResponse[AuthUserResponseSchema])
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db_session: Session = Depends(get_db_session)
) -> ApiResponse[AuthUserResponseSchema]:
    auth_service = AuthService(db_session=db_session)
    schema = LoginRequestSchema(
        email=form_data.username,
        password=form_data.password,
    )

    data = auth_service.login(schema=schema)

    return ApiResponse[AuthUserResponseSchema](
        content=data,
    )


@router.post(
    "/create-user",
    response_model=ApiResponse[UserResponseSchema],
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        schema: UserCreateRequestSchema,
        db_session: Session = Depends(get_db_session)
) -> ApiResponse[UserResponseSchema]:
    user_service = UserService(db_session=db_session)
    data = user_service.create(schema=schema)

    return ApiResponse[UserResponseSchema](
        status_code=status.HTTP_201_CREATED,
        content=data,
    )


@router.get("/me", response_model=ApiResponse[AuthUserResponseSchema])
async def get_auth_user(
        auth_user_response: AuthUserResponseSchema = Depends(auth_user)
) -> ApiResponse[AuthUserResponseSchema]:
    return ApiResponse[AuthUserResponseSchema](
        content=auth_user_response,
    )
