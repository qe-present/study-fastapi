from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI,Header

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/greet1/{name}")
async def greet(name: str):
    return {"message": f"Hello, {name}!"}


# 可选参数
@app.get('/greet/')
async def greet(
        name: Optional[str] = "john",
        age: Optional[int] = 30
) -> dict:
    return {"message": f"Hello, {name}!", "age": age}


class Book(BaseModel):
    title: str
    author: str


@app.post('/create_book')
async def create_book(book: Book):
    return {"title": book.title, "author": book.author}

@app.get('/get_header')
async def get_header(
        accept:str=Header(None),
        content_type=Header(None),
        user_agent=Header(None)
):
    request_headers={}
    request_headers['Accept']=accept
    request_headers['Content-Type']=content_type
    request_headers['User-Agent']=user_agent
    return request_headers

