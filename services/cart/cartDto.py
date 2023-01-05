from pydantic import BaseModel


class CartDto(BaseModel):
    user_profile_id: int
    cake_id: int
    quantity: int
