import enum

from pydantic import BaseModel


class Size(enum.Enum):
    Small = 1
    Medium = 2
    Large = 3


class Cake(BaseModel):
    id: int
    name: str
    price: int
    size: Size
    image: str
