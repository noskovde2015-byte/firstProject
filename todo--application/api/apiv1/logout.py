from fastapi import FastAPI, APIRouter, Response
from core.config import settings


router = APIRouter(prefix=settings.api.v1.exit,tags=["Auth"])
@router.post("")
async def logout_user(response: Response):
    response.delete_cookie(key="user_access_token")
    return {"message": "пользователь вышел из системы"}
