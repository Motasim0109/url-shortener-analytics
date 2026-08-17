from fastapi import FastAPI

app = FastAPI(
    title="URL Shortener Analytics",
    description="A URL shortener built one backend concept at a time.",
    version="0.1.0",
)


@app.get("/", tags=["general"])
def read_root() -> dict[str, str]:
    return {"message": "URL Shortener API"}


@app.get("/api/v1/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/api/v1/version",tags=["version"])
def get_version() -> dict[str, str]:
    return {"version": "0.1.0"}
