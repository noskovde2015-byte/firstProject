from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
import os
import shutil
from core.models import db_helper
from core.models import User
from core.schemas.Profile import ProfileRead
from auth.dependencies import get_current_user
from core.config import settings


UPLOAD_DIR = Path("uploads/avatars")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


router = APIRouter(prefix=settings.api.v1.profile, tags=["Profile"])

@router.get("", response_model=ProfileRead)
async def get_my_profile(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    return ProfileRead(
        id=current_user.id,
        name=current_user.name,
        avatar_url=current_user.avatar_url,
        email=current_user.email,
        age=current_user.age,
        created_at=current_user.created_at,
        post_count=current_user.post_count
    )


@router.post("")
async def upload_avatar(
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Only images are allowed")

    if file.size > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    file_extension = file.filename.split('.')[-1]
    filename = f"{current_user.id}_{int(datetime.utcnow().timestamp())}.{file_extension}"
    file_path = UPLOAD_DIR / filename


    try:
        with open(file_path, "wb") as buffer:
            # Читаем файл chunks чтобы не грузить память
            while content := await file.read(1024 * 1024):  # 1MB chunks
                buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

        # Обновляем avatar_url в базе
    try:
        current_user.avatar_url = f"/api/v1/profile/avatar/{filename}"
        await session.commit()
    except Exception as e:
        # Удаляем файл если не удалось обновить БД
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Error updating database: {str(e)}")

    return {
        "message": "Avatar uploaded successfully",
        "avatar_url": current_user.avatar_url
    }


@router.get("/avatar/{filename}")
async def get_avatar(filename: str):
    file_path = UPLOAD_DIR / filename

    # Проверяем что файл существует и находится в правильной директории
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Avatar not found")

    # Проверяем безопасность пути
    if ".." in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    return FileResponse(file_path)


@router.delete("/avatar")
async def delete_avatar(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    if not current_user.avatar_url:
        raise HTTPException(status_code=400, detail="No avatar to delete")

    # Извлекаем имя файла из URL
    filename = current_user.avatar_url.split("/")[-1]
    file_path = UPLOAD_DIR / filename

    # Удаляем файл если существует
    if file_path.exists():
        try:
            file_path.unlink()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

    # Обновляем базу данных
    current_user.avatar_url = None
    await session.commit()

    return {"message": "Avatar deleted successfully"}
