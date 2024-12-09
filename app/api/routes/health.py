from fastapi import APIRouter


router = APIRouter()


@router.get("/check")
async def hello_world():
    return {"message": "Up!"}
