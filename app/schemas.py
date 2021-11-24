from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class ResetPassword(UserCreate):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int  # User.id
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    Votes: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str


class UserEmail(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class VerifyCode(BaseModel):
    email: EmailStr
    reset_code: str


class isVerifyCode(BaseModel):
    verify_code: bool

    class Config:
        orm_mode = True


class VerifyEmail(BaseModel):
    email: EmailStr
    email_code: str


class isVerifyEmail(BaseModel):
    verify_email: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    phone_number: str
    first_name: str
    last_name: str
    city: str
    street: str
    house_number: str


class NewUpdateUser(UserUpdate):
    id: int
    phone_number: str
    first_name: str
    last_name: str
    city: str
    street: str
    house_number: str

    class Config:
        orm_mode = True


class Vote(BaseModel):

    post_id: int
    # grater than 0 and less than 1
    dir: conint(ge=0, le=1)

