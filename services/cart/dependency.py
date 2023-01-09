from boto3 import Session

from repositories.cart import add_to_cart, get_current_cart, clear_cart, mark_as_paid
from repositories.user import get_by_user_profile_id, get_by_user_id
from schema.cart import Cart
from services.cart.cartDto import CartDto
from services.respond import Respond


async def add_to_user_cart(payload: CartDto, db: Session):
    await get_by_user_profile_id(payload.user_profile_id, db)
    cart = await add_to_cart(payload, db)
    respond = Respond[Cart]()
    return respond.response(
        body=cart,
        code=201,
        message="Cart successfully added"
    )


async def get_cart(skip: int, limit: int, user_id: str, db: Session):
    user = get_by_user_id(user_id, db)
    cart = await get_current_cart(db, skip, limit, user.id)
    respond = Respond[Cart]()
    return respond.response(
        body=cart,
        code=200,
        message="Cart query successfully"
    )


async def clear_user_cart(db: Session, user_profile_id: int):
    result = await clear_cart(db, user_profile_id)
    respond = Respond[bool]()
    return respond.response(
        body=result,
        code=200,
        message="Cart query successfully"
    )


async def mark_user_cart_as_paid(db: Session, user_profile_id: int):
    result = await mark_as_paid(db, user_profile_id)
    respond = Respond[bool]()
    return respond.response(
        body=result,
        code=200,
        message="Cart query successfully"
    )

