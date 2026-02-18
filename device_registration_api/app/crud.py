from sqlalchemy.orm import Session

from . import models, schemas


def create_device(db: Session, device: schemas.DeviceRegister) -> models.Device:
    db_device = models.Device(userKey=device.userKey, deviceType=device.deviceType)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

