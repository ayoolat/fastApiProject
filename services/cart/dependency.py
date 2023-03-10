from boto3 import Session

from repositories.cart import add_to_cart, get_current_cart, clear_cart, mark_as_paid, remove_cake, get_all_orders, \
    mark_as_delivered, get_completed_orders
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


async def remove_one_cart_item(db: Session, cake_id: int, user_profile_id: int):
    result = await remove_cake(db, cake_id, user_profile_id)
    respond = Respond[bool]()
    return respond.response(
        body=result,
        code=200,
        message="Cart item removed successfully"
    )


async def mark_user_cart_as_paid(db: Session, user_profile_id: int):
    result = await mark_as_paid(db, user_profile_id)
    respond = Respond[bool]()
    return respond.response(
        body=result,
        code=200,
        message="Cart query successfully"
    )


async def mark_user_cart_as_delivered(db: Session, user_profile_id: int):
    result = await mark_as_delivered(db, user_profile_id)
    respond = Respond[bool]()
    return respond.response(
        body=result,
        code=200,
        message="Cart query successfully"
    )


async def get_all_cart_items(skip: int, limit: int, user_profile_id: int, db: Session):
    result = await get_all_orders(db, skip, limit, user_profile_id)
    respond = Respond[Cart]()
    return respond.response(
        body=result,
        code=200,
        message="Cart query successfully"
    )


async def get_all_completed_orders(skip: int, limit: int, user_profile_id: int, db: Session):
    result = await get_completed_orders(db, skip, limit, user_profile_id)
    respond = Respond[Cart]()
    return respond.response(
        body=result,
        code=200,
        message="Cart query successfully"
    )
