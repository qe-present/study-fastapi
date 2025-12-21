from sqlmodel import create_engine,text,SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from chapter04.config import settings


engine = AsyncEngine(
    create_engine(
        url=settings.DATABASE_URL,
        echo=True
    )
)
async def init_db():
    async with engine.begin() as conn:
        from ..book.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)
