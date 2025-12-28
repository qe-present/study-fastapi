import uuid
from datetime import datetime

from pydantic import BaseModel,Field

class User(BaseModel):
    username:str=Field(max_length=8)
    email:str=Field(max_length=40)
    password:str=Field(min_length=6)
    first_name:str=Field(max_length=30)
    last_name:str=Field(max_length=30)


class Register(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime