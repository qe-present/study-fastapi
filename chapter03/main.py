from fastapi import FastAPI
from .src.book import router as book_router

app = FastAPI()

app.include_router(book_router)





