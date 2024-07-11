from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from data.models.user import User


async def get_user_by_chat_id(session: AsyncSession, chat_id: int) -> User:
    async with session.begin():
        stmt = select(User).filter(User.chat_id == chat_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        return user


async def create_user(db: AsyncSession, username: str, email: str, hashed_password: str) -> User:
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[User]:
    stmt = select(User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()



