from secrets import token_urlsafe
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ShortLink
from app.schemas import ShortLinkCreate, ShortLinkResponse

app = FastAPI(
    title="URL Shortener Analytics",
    description="A URL shortener built one backend concept at a time.",
    version="0.1.0",
)


def generate_short_code() -> str:
    return token_urlsafe(8)


@app.get("/", tags=["general"])
def read_root() -> dict[str, str]:
    return {"message": "URL Shortener API"}


@app.get("/api/v1/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/version", tags=["version"])
def get_version() -> dict[str, str]:
    return {"version": "0.1.0"}


@app.post("/api/v1/links", tags=["links"], response_model=ShortLinkResponse, status_code=201)
def generate_link(
    slc: ShortLinkCreate,
    session: Annotated[Session, Depends(get_db)],
) -> ShortLink:
    sl = ShortLink(destination_url=str(slc.destination_url), short_code=generate_short_code())
    session.add(sl)
    session.commit()
    session.refresh(sl)

    return sl


@app.get("/api/v1/links", tags=["links"], response_model=list[ShortLinkResponse])
def get_links(session: Annotated[Session, Depends(get_db)]) -> list[ShortLink]:
    return session.scalars(select(ShortLink).order_by(ShortLink.id)).all()
