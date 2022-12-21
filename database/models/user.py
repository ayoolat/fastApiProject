from sqlalchemy import Column, Integer, String, UniqueConstraint

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(70), unique=True, nullable=False)
    user_id = Column(String(40), nullable=False)

