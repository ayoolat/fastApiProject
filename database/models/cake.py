from sqlalchemy import Column, Integer, String

from database.database import Base


class Cake(Base):
    __tablename__ = "cakes"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    body = Column(String(50))
