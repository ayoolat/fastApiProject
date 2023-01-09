from sqlalchemy.orm import Session

from services.cart.cartDto import CartDto
from database.models.cart import Cart


async def add_to_cart(payload: CartDto, db: Session):
    new_cart = Cart(
        cake_id=payload.cake_id,
        user_profile_id=payload.user_profile_id,
        paid=False,
        delivered=False,
        quantity=payload.quantity
    )
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart


async def get_current_cart(db: Session, skip: int, limit: int, user_profile_id: int):
    cart = db.query(Cart)\
        .filter(Cart.paid is False)\
        .filter( Cart.user_profile_id == "")\
        .offset(limit * (skip - 1))\
        .limit(limit)\
        .all()
    print(cart)
    return cart


async def clear_cart(db: Session, user_profile_id: int):
    carts = db.query(Cart).filter(Cart.user_profile_id == user_profile_id).all()
    for cart in carts:
        db.delete(cart)
    db.commit()
    return True


async def mark_as_paid(db: Session, user_profile_id: int):
    carts = db.query(Cart).filter(Cart.user_profile_id == user_profile_id).all()
    for cart in carts:
        await cart_update(db, cart)
    db.commit()
    return True


async def cart_update(db: Session, payload: Cart):
    cart = await db.query(Cart).filter(Cart.id == payload.id).first()
    cart_data = payload.dict(exclude_unset=True)
    for key, value in cart_data.items():
        setattr(cart, key, value)

    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart_data
