import uuid
from datetime import datetime, date

from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    publisher: str
    publish_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime


class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None

class CreateBook(BaseModel):
    title: str
    author: str
    publisher: str
    publish_date: str
    page_count: int
    language: str