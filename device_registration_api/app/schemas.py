from pydantic import BaseModel

from common.device_types import DeviceType


class DeviceRegister(BaseModel):
    userKey: str
    deviceType: DeviceType
