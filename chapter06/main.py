from fastapi import FastAPI
from .src.auth import user_roter
app = FastAPI()
app.include_router(user_roter)


