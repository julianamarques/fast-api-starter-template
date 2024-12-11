from fastapi import APIRouter

from app.api.responses import ApiResponse


router = APIRouter()


@router.get("/check", response_model=ApiResponse)
async def health_check() -> ApiResponse:
    return ApiResponse(content="Up!")
