from sqlalchemy import Column, Integer, String, Enum

from database.database import Base
from schema.cake import Size


class Cake(Base):
    __tablename__ = "cakes"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(Integer, nullable=False)
    size = Column(Enum(Size), nullable=False)
    image = Column(String(200), nullable=False)
