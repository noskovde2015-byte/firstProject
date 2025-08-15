from fastapi import APIRouter
from core.config import settings
from .register_view import router as register_router

router = APIRouter(prefix=settings.api.v1.prefix)
router.include_router(register_router)