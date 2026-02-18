import os

import httpx
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from common.device_types import DeviceType

from . import crud, schemas
from .database import SessionLocal

app = FastAPI()

DEVICE_REGISTRATION_API_HOST = os.getenv(
    "DEVICE_REGISTRATION_API_HOST", "device_registration_api"
)
DEVICE_REGISTRATION_API_URL = (
    f"http://{DEVICE_REGISTRATION_API_HOST}:8000/Device/register"
)
ALLOWED_DEVICE_TYPES = {dt.value for dt in DeviceType}


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
    "/Log/auth",
    response_model=schemas.LogAuthResponse,
    status_code=status.HTTP_200_OK,
)
async def log_auth(event: schemas.LoginEvent):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                DEVICE_REGISTRATION_API_URL,
                json={"userKey": event.userKey, "deviceType": event.deviceType},
            )
            response.raise_for_status()
        except (httpx.RequestError, httpx.HTTPStatusError):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"statusCode": 400, "message": "bad_request"},
            )

    return schemas.LogAuthResponse(statusCode=200, message="success")


@app.get(
    "/Log/auth/statistics",
    response_model=schemas.StatisticsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_statistics(deviceType: str):
    count = -1
    db = SessionLocal()
    try:
        if deviceType in ALLOWED_DEVICE_TYPES:
            count = crud.get_device_count_by_type(db, deviceType)
    except Exception:
        count = -1
    finally:
        db.close()

    return schemas.StatisticsResponse(deviceType=deviceType, count=count)
