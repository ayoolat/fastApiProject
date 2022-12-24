from fastapi import HTTPException
from sqlalchemy.orm import Session

from schema import cake
from database.models.cake import Cake
from services.cake.updateCake import CakeUpdate


async def add_cake(payload: cake.Cake, db: Session):
    new_cake = Cake(name=payload.name, price=payload.price, size=payload.size)
    db.add(new_cake)
    db.commit()
    db.refresh(new_cake)
    return new_cake


async def get_all_cakes(db: Session, skip: int, limit: int):
    cakes = db.query(Cake).offset(skip).limit(limit).all()
    return cakes


async def get_one_cake(db: Session, id: int):
    cake = await db.query(Cake).filter(Cake.id == id).first()
    if not cake:
        raise HTTPException(status_code=404, detail="Cake not found")
    return cake


async def update_cake(db: Session, payload: CakeUpdate):
    cake = await get_one_cake(db, payload.id)
    cake_data = payload.dict(exclude_unset=True)
    for key, value in cake_data.items():
        setattr(cake, key, value)
    db.add(payload)
    db.commit()
    db.refresh(payload)
    return payload


async def delete_cake(db: Session, id: int):
    cake = await get_one_cake(db, id)
    db.delete(cake)
    db.commit()
    return True