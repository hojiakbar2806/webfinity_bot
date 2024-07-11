from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from data.config import settings

# Create async engine using asyncpg
async_engine = create_async_engine(settings.db_url_asyncpg, echo=False)

# Create async session maker
async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False  # Adjust as needed
)

Base = declarative_base()


# Async context manager for session
@asynccontextmanager
async def get_session():
    async_session = async_session_maker()
    try:
        yield async_session
        await async_session.commit()
    except Exception as e:
        await async_session.rollback()
        raise e
    finally:
        await async_session.close()
