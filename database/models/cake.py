from sqlalchemy import Column, Integer, String

from database.database import Base


class Cake(Base):
    __tablename__ = "cakes"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Integer)
    size = Column(String(50))
