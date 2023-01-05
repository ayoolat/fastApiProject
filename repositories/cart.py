from sqlalchemy.orm import Session

from schema.cart import Cart
from services.cart.cartDto import CartDto


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
    cakes = db.query(Cart) \
        .filter(Cart.paid == False, Cart.user_profile_id == user_profile_id) \
        .offset(limit * (skip - 1)) \
        .limit(limit)\
        .all()
    return cakes


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
