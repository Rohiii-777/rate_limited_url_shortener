from pydantic import BaseModel, EmailStr,HttpUrl
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class URLCreate(BaseModel):
    url: HttpUrl

class URLInfo(BaseModel):
    short_id: str
    original_url: HttpUrl
    owner_id: Optional[int]
    ip_address: Optional[str]

    class Config:
        orm_mode = True