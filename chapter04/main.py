from fastapi import FastAPI
from contextlib import asynccontextmanager
from .src.db.main import init_db
@asynccontextmanager
async def life_span(app: FastAPI):
    print("Starting up...")
    await init_db()
    yield
    print("Shutting down...")



app = FastAPI(
    title="Bookly",
    lifespan=life_span,
)