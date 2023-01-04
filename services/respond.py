from typing import TypeVar, Generic

from schema.response import ResponseDTO

T = TypeVar('T')


class Respond(Generic[T]):
    def __init__(self) -> None:
        self._items = []

    def response(self, body: T, code: int, message: str):
        response = ResponseDTO[str](body=body, code=code, message=message)
        return response
