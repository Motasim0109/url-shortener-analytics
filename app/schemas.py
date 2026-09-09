from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl


class ShortLinkCreate(BaseModel):
    destination_url: HttpUrl


class ShortLinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    destination_url: str
    short_code: str
    created_at: datetime


class ShortLinkAnalytics(BaseModel):
    short_code: str
    destination_url: str
    click_count: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
