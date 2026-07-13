from fastapi import APIRouter

from app.api.responses import ApiResponse


router = APIRouter()


@router.get("/check", response_model=ApiResponse[str])
async def health_check() -> ApiResponse[str]:
    return ApiResponse(content="Up!")
