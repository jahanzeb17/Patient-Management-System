from sqlalchemy import Boolean, Column, Integer, String, Float
from database import Base


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String(50))
    city = Column(String(50))
    age = Column(Integer)
    gender = Column(String(50))
    height = Column(Float)
    weight = Column(Float)
    bmi = Column(Float)
    verdict = Column(String(50))