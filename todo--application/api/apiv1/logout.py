from fastapi import FastAPI, APIRouter, Response,Depends

from auth.dependencies import get_current_user
from core.config import settings
from core.logger_settings.logger import logger
from core.models import User

router = APIRouter(prefix=settings.api.v1.exit,tags=["Auth"])
@router.post("")
async def logout_user(response: Response,current_user: User = Depends(get_current_user)):
    response.delete_cookie(key="user_access_token")
    logger.info(f"Пользователь {current_user.email} вышел из системы")
    return {"message": "пользователь вышел из системы"}
