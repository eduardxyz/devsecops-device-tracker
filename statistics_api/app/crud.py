from sqlalchemy.orm import Session

from . import models


def get_device_count_by_type(db: Session, device_type: str) -> int:
    return (
        db.query(models.Device)
        .filter(models.Device.deviceType == device_type)
        .count()
    )

