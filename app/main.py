from datetime import UTC, datetime
from secrets import token_urlsafe
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ClickEvent, ShortLink, User
from app.schemas import (
    ShortLinkAnalytics,
    ShortLinkCreate,
    ShortLinkResponse,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.security import (
    DUMMY_PASSWORD_HASH,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

bearer_scheme = HTTPBearer(auto_error=False)
RESERVED_SHORT_CODES = {"docs", "redoc"}

app = FastAPI(
    title="URL Shortener Analytics",
    description="A URL shortener built one backend concept at a time.",
    version="0.1.0",
)


def generate_short_code() -> str:
    return token_urlsafe(8)


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    session: Annotated[Session, Depends(get_db)],
) -> User:
    exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise exception

    decoded_credentials = decode_access_token(credentials.credentials)
    if decoded_credentials is None:
        raise exception

    user = session.get(User, decoded_credentials)
    if user is None:
        raise exception

    return user


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
    current_user: Annotated[User, Depends(get_current_user)],
    slc: ShortLinkCreate,
    session: Annotated[Session, Depends(get_db)],
) -> ShortLink:
    if slc.custom_alias in RESERVED_SHORT_CODES:
        raise HTTPException(status_code=409, detail="Custom alias is reserved")
    for _ in range(5):
        try:
            sl = ShortLink(
                destination_url=str(slc.destination_url),
                short_code=slc.custom_alias or generate_short_code(),
                owner_id=current_user.id,
                expires_at=slc.expires_at,
            )

            session.add(sl)
            session.commit()
        except IntegrityError:
            session.rollback()

            if slc.custom_alias is not None:
                raise HTTPException(status_code=409, detail="Custom alias already in use") from None

            continue
        else:
            session.refresh(sl)
            return sl

    raise HTTPException(status_code=500, detail="Could not generate a unique short code")


@app.post("/api/v1/auth/signup", tags=["auth"], response_model=UserResponse, status_code=201)
def create_user(
    user: UserCreate,
    session: Annotated[Session, Depends(get_db)],
) -> User:
    new_user = User(
        email=str(user.email).lower(),
        hashed_password=hash_password(user.password),
    )
    session.add(new_user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Email already registered") from None

    session.refresh(new_user)
    return new_user


@app.get("/api/v1/links", tags=["links"], response_model=list[ShortLinkResponse])
def get_links(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_db)],
) -> list[ShortLink]:
    return session.scalars(
        select(ShortLink).where(ShortLink.owner_id == current_user.id).order_by(ShortLink.id)
    ).all()


@app.post("/api/v1/auth/login", tags=["auth"], response_model=TokenResponse)
def login(user: UserLogin, session: Annotated[Session, Depends(get_db)]) -> TokenResponse:
    email = str(user.email).lower()
    retrieved_user = session.scalar(select(User).where(User.email == email))

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if retrieved_user is None:
        verify_password(user.password, DUMMY_PASSWORD_HASH)
        raise credentials_exception

    if not verify_password(user.password, retrieved_user.hashed_password):
        raise credentials_exception

    new_token = create_access_token(retrieved_user.id)
    return TokenResponse(access_token=new_token)


@app.get("/api/v1/auth/me", tags=["auth"], response_model=UserResponse)
def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user


@app.get("/{short_code}", tags=["redirects"])
def get_short_code(
    short_code: str,
    session: Annotated[Session, Depends(get_db)],
) -> RedirectResponse:
    short_link = session.scalar(select(ShortLink).where(ShortLink.short_code == short_code))

    if short_link is None:
        raise HTTPException(status_code=404, detail="Short link not found!")

    if short_link.expires_at is not None and short_link.expires_at <= datetime.now(UTC):
        raise HTTPException(status_code=410, detail="Short link has expired")

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
    current_user: Annotated[User, Depends(get_current_user)],
    short_code: str,
    session: Annotated[Session, Depends(get_db)],
) -> ShortLinkAnalytics:
    short_link = session.scalar(
        select(ShortLink).where(
            ShortLink.short_code == short_code, ShortLink.owner_id == current_user.id
        )
    )

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
