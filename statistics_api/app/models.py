from sqlalchemy import Column, Integer, String

from .database import Base


class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    userKey = Column(String, index=True)
    deviceType = Column(String, index=True)
