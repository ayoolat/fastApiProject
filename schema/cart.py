from pydantic import BaseModel


class Cake(BaseModel):
    id: int
    user_profile_id: int
    cake_id: int
    paid: bool
    delivered: bool
    quantity: int
