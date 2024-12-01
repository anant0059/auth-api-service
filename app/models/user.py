from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    id: str
