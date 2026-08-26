from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


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
