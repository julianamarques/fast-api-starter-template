from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.responses import ApiResponse
from app.depends import get_db_session, get_current_user
from app.schemas import UserCreateSchema, LoginSchema, CurrentUserSchema
from app.services.auth_service import AuthService


router = APIRouter()


@router.post("/create-user", response_model=ApiResponse)
async def create_user(user: UserCreateSchema, db_session: Session = Depends(get_db_session)) -> ApiResponse:
    auth_service = AuthService(db_session=db_session)
    auth_service.create(schema=user)

    return ApiResponse()


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db_session: Session = Depends(get_db_session)) -> ApiResponse:
    auth_service = AuthService(db_session=db_session)
    schema = LoginSchema(
        email=form_data.username,
        password=form_data.password
    )

    data = auth_service.login(schema=schema)

    return ApiResponse(
        content=data,
    )


@router.get("/me")
async def get_current_user(current_user: CurrentUserSchema = Depends(get_current_user)) -> ApiResponse:
    return ApiResponse(
        content=current_user,
    )
