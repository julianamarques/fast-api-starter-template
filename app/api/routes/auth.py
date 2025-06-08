from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.responses import ApiResponse
from app.core.database_config import Session
from app.depends import get_db_session, get_auth_user
from app.schemas.auth_schema import (
    AuthUserResponseSchema,
    LoginRequestSchema,
    UserCreateRequestSchema
)
from app.services.auth_service import AuthService
from app.services.user_service import UserService


router = APIRouter()


@router.post("/login", response_model=ApiResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db_session: Session = Depends(get_db_session)) -> ApiResponse:
    auth_service = AuthService(db_session=db_session)
    schema = LoginRequestSchema(
        email=form_data.username,
        password=form_data.password,
    )

    data = auth_service.login(schema=schema)

    return ApiResponse(
        content=data,
    )


@router.post("/create-user", response_model=ApiResponse)
async def create_user(schema: UserCreateRequestSchema,
                      db_session: Session = Depends(get_db_session)) -> ApiResponse:
    user_service = UserService(db_session=db_session)
    data = user_service.create(schema=schema)

    return ApiResponse(
        content=data,
    )


@router.get("/me", response_model=ApiResponse)
async def get_auth_user(auth_user: AuthUserResponseSchema = Depends(get_auth_user)) -> ApiResponse:
    return ApiResponse(
        content=auth_user,
    )
