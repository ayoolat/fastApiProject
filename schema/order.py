from pydantic import BaseModel


class Order(BaseModel):
    user_profile_id: int
    cart_id: int
