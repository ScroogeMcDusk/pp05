from sqlalchemy import Column, Integer, String, Float
from database import Base

class Tire(Base):
    __tablename__ = "tires"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    diameter = Column(Float)
    pressure = Column(Float)
    status = Column(String)