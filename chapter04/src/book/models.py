import uuid
from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel, Field,Column
import sqlalchemy.dialects.postgresql as pg

class Book(SQLModel,table=True):
    __tablename__ = 'books'
    id: UUID=Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4(),
        )
    )
    title: str
    author: str
    publisher: str
    publish_date: str
    page_count: int
    language: str
    created_at: datetime=Field(
        Column(
            pg.TIMESTAMP,
            default=datetime.now(),
        )
    )
    updated_at: datetime=Field(
        Column(
            pg.TIMESTAMP,
            default=datetime.now(),
        )
    )
    def __repr__(self):
        return f'<Book(id={self.id}, title={self.title})>'