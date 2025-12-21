from fastapi import APIRouter, HTTPException, status
from typing import List
from .schemas import Book, UpdateBook
from .data import books

# 创建路由实例
router = APIRouter(prefix="/books", tags=["books"])


@router.get('/', response_model=List[Book])
async def get_books():
    return books


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_book(book: Book):
    # 转换为字典后添加到内存数据库
    books.append(book.model_dump())
    return book


@router.get('/{book_id}')
async def get_book(book_id: int):
    # 修复变量名冲突：用 b 而不是 book
    found_book = next((b for b in books if b['id'] == book_id), None)
    if not found_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return found_book


@router.patch('/{book_id}')
async def update_book(book_id: int, book_data: UpdateBook):
    # 修复变量名冲突
    now_book = next((b for b in books if b['id'] == book_id), None)
    if not now_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    # 修复：排除未设置和为 None 的字段
    update_data = book_data.model_dump(exclude_unset=True, exclude_none=True)
    if not update_data:
        return now_book

    now_book.update(update_data)
    return now_book


@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    # 修复变量名冲突
    now_book = next((b for b in books if b['id'] == book_id), None)
    if not now_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    books.remove(now_book)
    # 204 状态码不应该返回内容
    return None