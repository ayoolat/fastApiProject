from sqlalchemy import Integer, ForeignKey, ForeignKeyConstraint, Column
from sqlalchemy.orm import relationship

from database.database import Base


class Order(Base):
    __tablename__ = "orders"

    user_profile_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    cart_id = Column(Integer, ForeignKey("carts.id"), primary_key=True, nullable=False)

    user = relationship("User")
    cart = relationship("Cart")