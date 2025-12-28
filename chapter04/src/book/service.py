from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import CreateBook, UpdateBook
from .models import Book
from sqlmodel import select, desc
from datetime import datetime

class BookService:
    # noinspection PyMethodMayBeStatic
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.updated_at))
        results = await session.execute(statement)
        return results.scalars().all()

    # noinspection PyMethodMayBeStatic
    async def get(self, uid: str, session: AsyncSession):
        statement = select(Book).where(Book.id == uid)
        results = await session.execute(statement)
        return results.scalar_one_or_none()

    # noinspection PyMethodMayBeStatic
    async def create(self, data: CreateBook, session: AsyncSession):
        data_dict=data.model_dump()
        new_book = Book(**data_dict)

        new_book.publish_date=datetime.strptime(data_dict['publish_date'], "%Y-%m-%d").date()

        session.add(new_book)
        await session.commit()
        return new_book

    async def update(self, uid: str, data: UpdateBook, session: AsyncSession):
        book = await self.get(uid, session)
        if not book:
            return None
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:  # 如果没有提供任何更新字段
            return book
        for key, value in update_data.items():
            setattr(book, key, value)
        await session.commit()
        return book

    async def delete(self, uid: str, session: AsyncSession):
        book = await self.get(uid, session)
        if not book:
            return None
        await session.delete(book)
        await session.commit()
        return book
