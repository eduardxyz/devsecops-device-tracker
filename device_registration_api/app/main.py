import os

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from . import crud, schemas
from .database import Base, SessionLocal, engine

app = FastAPI()


@app.on_event("startup")
def startup() -> None:
    if os.getenv("AUTO_CREATE_TABLES", "").lower() in {"1", "true", "yes", "on"}:
        Base.metadata.create_all(bind=engine)


@app.get("/healthz")
async def healthz():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(status_code=503, content={"status": "unhealthy"})
    finally:
        db.close()

    return {"status": "ok"}


@app.post(
    "/Device/register",
    response_model=schemas.RegisterResponse,
    status_code=status.HTTP_200_OK,
)
async def register_device(device: schemas.DeviceRegister):
    db = SessionLocal()
    try:
        crud.create_device(db, device)
        return schemas.RegisterResponse(statusCode=200)
    except Exception:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"statusCode": 400},
        )
    finally:
        db.close()
