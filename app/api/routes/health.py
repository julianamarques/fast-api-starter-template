from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.responses import ApiResponse
from app.core.database_config import Session
from app.depends import get_db_session
from app.enums import ApiMessageEnum
from app.utils import exceptions_utils


router = APIRouter()


@router.get("/check", response_model=ApiResponse[str])
async def health_check(db_session: Session = Depends(get_db_session)) -> ApiResponse[str]:
    try:
        db_session.execute(text("SELECT 1"))

        return ApiResponse[str](content="Up!")
    except SQLAlchemyError:
        exceptions_utils.raise_service_unavailable(ApiMessageEnum.EXTERNAL_UNAVAILABLE_SERVICE.value)
