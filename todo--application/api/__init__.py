from fastapi import APIRouter
from core.config import settings
from api.apiv1 import router as apiv1_router

router = APIRouter(prefix=settings.api.prefix)
router.include_router(apiv1_router)