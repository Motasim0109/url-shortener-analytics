from secrets import token_urlsafe
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ClickEvent, ShortLink
from app.schemas import ShortLinkAnalytics, ShortLinkCreate, ShortLinkResponse

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
    for _ in range(5):
        try:
            sl = ShortLink(
                destination_url=str(slc.destination_url), short_code=generate_short_code()
            )
            session.add(sl)
            session.commit()
        except IntegrityError:
            session.rollback()
            continue
        else:
            session.refresh(sl)
            return sl

    raise HTTPException(status_code=500, detail="Could not generate a unique short code")


@app.get("/api/v1/links", tags=["links"], response_model=list[ShortLinkResponse])
def get_links(session: Annotated[Session, Depends(get_db)]) -> list[ShortLink]:
    return session.scalars(select(ShortLink).order_by(ShortLink.id)).all()


@app.get("/{short_code}", tags=["redirects"])
def get_short_code(
    short_code: str,
    session: Annotated[Session, Depends(get_db)],
) -> RedirectResponse:
    short_link = session.scalar(select(ShortLink).where(ShortLink.short_code == short_code))

    if short_link is None:
        raise HTTPException(status_code=404, detail="Short link not found!")

    event = ClickEvent(short_link_id=short_link.id)
    session.add(event)
    session.commit()

    return RedirectResponse(
        url=short_link.destination_url,
        status_code=307,
    )


@app.get(
    "/api/v1/links/{short_code}/analytics", tags=["analytics"], response_model=ShortLinkAnalytics
)
def get_link_analytics(
    short_code: str,
    session: Annotated[Session, Depends(get_db)],
) -> ShortLinkAnalytics:
    short_link = session.scalar(select(ShortLink).where(ShortLink.short_code == short_code))

    if short_link is None:
        raise HTTPException(status_code=404, detail="Short link not found!")

    click_count = session.scalar(
        select(func.count(ClickEvent.id)).where(ClickEvent.short_link_id == short_link.id)
    )

    return ShortLinkAnalytics(
        short_code=short_link.short_code,
        destination_url=short_link.destination_url,
        click_count=click_count or 0,
    )
