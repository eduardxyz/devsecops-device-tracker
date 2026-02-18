from pydantic import BaseModel

from common.device_types import DeviceType


class LoginEvent(BaseModel):
    userKey: str
    deviceType: DeviceType


class LogAuthResponse(BaseModel):
    statusCode: int
    message: str


class StatisticsResponse(BaseModel):
    deviceType: str
    count: int
