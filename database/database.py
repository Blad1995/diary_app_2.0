import os
from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import database_settings

DATABASE_URL = f'postgresql+asyncpg://{os.getenv("DATABASE_URL", "postgres:postgres@localhost:5432/diary")}'


engine = create_async_engine(
    DATABASE_URL,
    echo=database_settings.echo,
)

async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
async_session = async_scoped_session(async_session_maker, scopefunc=current_task)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yields an async session."""
    async with async_session() as session:
        yield session
