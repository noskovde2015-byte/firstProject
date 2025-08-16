from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models import db_helper
from core.config import settings
from auth.authShchema import AuthSchema
from auth.auth import hash_password, verify_password, authenticate_user, create_access_token



router = APIRouter(prefix=settings.api.v1.log, tags=["Auth"])

@router.post("")
async def login_user(user_data: AuthSchema,
                    response: Response,
                     session: AsyncSession = Depends(db_helper.session_getter),
                      ):
    check = await authenticate_user(
        session=session,
        email=user_data.email,
        password=user_data.password,
    )

    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",

        )
    access_token = create_access_token(
        {"sub": str(check.id)},
    )
    response.set_cookie(key="user_access_token", value=access_token, httponly=True)
    return {"access_token": access_token}

