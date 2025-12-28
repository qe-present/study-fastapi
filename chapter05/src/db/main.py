from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlmodel import SQLModel
from chapter04.config import settings

# 创建异步引擎
engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,
)

# 创建异步 sessionmaker
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 初始化数据库
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# FastAPI 依赖
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI 依赖注入，自动管理会话生命周期"""
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()