from typing import List, Optional

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

app = FastAPI()
books = [
    {
        'id': 1,
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'publisher': 'Scribner',
        'publish_date': '1925-04-10',
        'page_count': 218,
        'language': 'English'
    },
    {
        'id': 2,
        'title': 'The Shadow of Yesterday',
        'author': 'Eleanor Whitmore',
        'publisher': 'Penguin Random House',
        'publish_date': '2019-08-15',
        'page_count': 342,
        'language': 'English'
    },
    {
        'id': 3,
        'title': 'La Orilla del Silencio',
        'author': 'María del Carmen Fuentes',
        'publisher': 'Alfaguara',
        'publish_date': '2021-03-22',
        'page_count': 287,
        'language': 'Spanish'
    },
    {
        'id': 4,
        'title': 'Machine Learning for Everyone',
        'author': 'Dr. James Chen',
        'publisher': "O'Reilly Media",
        'publish_date': '2023-01-10',
        'page_count': 456,
        'language': 'English'
    },
    {
        'id': 5,
        'title': 'The Clockwork Dragon',
        'author': 'Victoria Ashford',
        'publisher': 'HarperCollins',
        'publish_date': '2020-11-05',
        'page_count': 512,
        'language': 'English'
    },
    {
        'id': 6,
        'title': 'Under the Cherry Moon',
        'author': 'Takeshi Nakamura',
        'publisher': 'Kodansha',
        'publish_date': '2018-06-30',
        'page_count': 194,
        'language': 'Japanese'
    }
]


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    publish_date: str
    page_count: int
    language: str


class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None


@app.get('/books', response_model=List[Book])
async def get_books():
    return books


@app.post('/books')
async def add_book(book: Book, status_code=status.HTTP_201_CREATED):
    books.append(book.model_dump())
    return book


@app.get('/books/{book_id}')
async def get_book(book_id: int):
    book = next((book for book in books if book['id'] == book_id), None)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@app.patch('/books/{book_id}')
async def update_book(book_id: int, book: UpdateBook):
    now_book = next((book for book in books if book['id'] == book_id), None)
    if not now_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    # 2. 只更新提供的字段（排除 None 值）
    update_data = book.model_dump(exclude_unset=True)  # 关键！
    if not update_data:
        return book  # 没有提供任何更新字段
    now_book.update(update_data)
    return now_book



@app.delete('/books/{book_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    now_book=next((book for book in books if book['id']==book_id),None)
    if not now_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    books.remove(now_book)
