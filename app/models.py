from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ShortLink(Base):
    __tablename__ = "short_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    destination_url: Mapped[str] = mapped_column(String(2048))
    short_code: Mapped[str] = mapped_column(String(12), index=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
