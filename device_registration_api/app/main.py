import os

from fastapi import FastAPI
from sqlalchemy import text

from .database import Base, SessionLocal, engine

app = FastAPI()


@app.on_event("startup")
def startup() -> None:
    if os.getenv("AUTO_CREATE_TABLES", "").lower() in {"1", "true", "yes", "on"}:
        Base.metadata.create_all(bind=engine)
