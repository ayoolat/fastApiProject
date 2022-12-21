from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    paid = Column(Boolean, default=False)
    delivered = Column(Boolean, default=False)
    quantity = Column(Integer)
    cake_id = Column(Integer, ForeignKey("cakes.id"))
    user_profile_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")
    cake = relationship("Cake")
