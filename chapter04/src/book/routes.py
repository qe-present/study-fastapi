from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UpdateBook, CreateBook,Book
from chapter04.src.db.main import get_session
from .service import BookService

router = APIRouter(prefix="/books", tags=["books"])
service = BookService()


@router.get('/', response_model=List[Book])
async def get_books(session: AsyncSession = Depends(get_session)):
    books = await service.get_all_books(session)
    return books


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Book)
async def add_book(book: CreateBook, session: AsyncSession = Depends(get_session)):
    new_book = await service.create(book, session)  # ✅ 添加 await
    return new_book


@router.get('/{book_id}', response_model=Book)
async def get_book(book_id: str, session: AsyncSession = Depends(get_session)):
    found_book = await service.get(book_id, session)  # ✅ 添加 await
    if not found_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return found_book


@router.patch('/{book_id}', response_model=Book)
async def update_book(book_id: str, book_data: UpdateBook, session: AsyncSession = Depends(get_session)):  # ✅ 添加 session
    updated_book = await service.update(book_id, book_data, session)  # ✅ 添加 await
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return updated_book


@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, session: AsyncSession = Depends(get_session)):  # ✅ 添加 session
    await service.delete(book_id, session)  # ✅ 添加 await，移除无用变量
    return None