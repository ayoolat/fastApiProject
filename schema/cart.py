from pydantic import BaseModel


class Cart(BaseModel):
    user_profile_id: int
    cake_id: int
    paid: bool
    delivered: bool
    quantity: int
