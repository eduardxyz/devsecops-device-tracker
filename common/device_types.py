from enum import Enum

class DeviceType(str, Enum):
    iOS = "iOS"
    Android = "Android"
    Watch = "Watch"
    TV = "TV"
