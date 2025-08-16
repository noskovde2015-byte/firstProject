from fastapi import APIRouter
from core.config import settings
from .register_view import router as register_router
from .user_views import router as user_router
from .login_views import router as login_router
from .post_views import router as post_router

router = APIRouter(prefix=settings.api.v1.prefix)


router.include_router(register_router)
router.include_router(user_router)
router.include_router(login_router)
router.include_router(post_router)