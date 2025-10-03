import typer
import asyncio
from sqlalchemy import select
from pathlib import Path
import sys

# Добавляем путь к проекту
sys.path.append(str(Path(__file__).parent.parent.parent))

from core.models import User, Role
from core.models import db_helper

app = typer.Typer()


async def _assign_default_roles():
    """Асинхронная логика назначения ролей"""
    async with db_helper.session_factory() as session:
        user_role = await session.scalar(select(Role).where(Role.name == "user"))
        if not user_role:
            typer.echo("❌ Роль 'user' не существует! Создайте её сначала.")
            raise typer.Exit(code=1)

        # Обновляем всех пользователей без роли
        result = await session.execute(
            select(User).where(User.role_id.is_(None))
        )
        users = result.scalars().all()

        for user in users:
            user.role_id = user_role.id

        await session.commit()
        typer.echo(f"✅ Назначена роль 'user' для {len(users)} пользователей")


@app.command(name="assign-default-roles")
def assign_default_roles():
    """Назначить всем пользователям роль 'user'"""
    asyncio.run(_assign_default_roles())


if __name__ == "__main__":
    app()