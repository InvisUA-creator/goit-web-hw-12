from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.dbase.dbase import get_db
from src.dbase.models import User
from src.schemas.user import UserSchema


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image_url()
    except Exception ass err:
        print(f"Error getting Gravatar for {body.email}: {err}")

    new_user = User(**body.model_dump(), avatar=avatar)
    await db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    if token:
        user.refresh_token = token
    else:
        user.refresh_token = None
    await db.commit()
    await db.refresh(user)