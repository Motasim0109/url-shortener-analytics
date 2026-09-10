from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, field_validator


class ShortLinkCreate(BaseModel):
    destination_url: HttpUrl
    custom_alias: str | None = Field(
        default=None, min_length=3, max_length=12, pattern=r"^[A-Za-z0-9_-]+$"
    )
    expires_at: datetime | None = None

    @field_validator("expires_at")
    @classmethod
    def validate_expires_at(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None

        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("expires_at must include timezone")

        if value <= datetime.now(UTC):
            raise ValueError("expires_at must be in the future")

        return value


class ShortLinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    destination_url: str
    short_code: str
    created_at: datetime
    expires_at: datetime | None


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
