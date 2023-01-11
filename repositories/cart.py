from fastapi import HTTPException
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
        .filter(Cart.user_profile_id == user_profile_id)\
        .filter(Cart.paid == False)\
        .offset(limit * (skip - 1))\
        .limit(limit)\
        .all()
    return cart


async def remove_cake(db: Session, cart_id: int, user_profile_id: int):
    cart = db.query(Cart)\
        .filter(Cart.user_profile_id == user_profile_id)\
        .filter(Cart.paid == False)\
        .filter(Cart.id == cart_id)\
        .first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(cart)
    db.commit()
    return True


async def clear_cart(db: Session, user_profile_id: int):
    carts = db.query(Cart)\
        .filter(Cart.user_profile_id == user_profile_id)\
        .filter(Cart.paid == False)\
        .all()
    for cart in carts:
        db.delete(cart)
    db.commit()
    return True


async def mark_as_paid(db: Session, user_profile_id: int):
    carts = db.query(Cart)\
        .filter(Cart.user_profile_id == user_profile_id)\
        .filter(Cart.paid == False)\
        .all()

    for cart in carts:
        cart.paid = True
        cart_update(db, cart)
    db.commit()
    return True


def cart_update(db: Session, payload: Cart):
    db.add(payload)
    db.commit()
    db.refresh(payload)
    return payload
