from fastapi import HTTPException
from sqlalchemy.orm import Session

from schema import cake
from database.models.cake import Cake
from services.cake.updateCake import CakeUpdate


async def add_cake(payload: cake.Cake, db: Session):
    new_cake = Cake(name=payload.name, price=payload.price, size=payload.size, image=payload.image)
    db.add(new_cake)
    db.commit()
    db.refresh(new_cake)
    return new_cake


async def get_all_cakes(db: Session, skip: int, limit: int):
    cakes = db.query(Cake).offset(limit * (skip - 1)).limit(limit).all()
    print(cakes)
    return cakes


async def count_all_cakes(db: Session):
    number = db.query(Cake).count()
    return number


async def count_cake(db: Session, id: int):
    number = db.query(Cake).filter(Cake.id == id).count()
    print(number)
    if number > 0:
        return True
    raise HTTPException(status_code=404, detail="Cake not found")


async def get_one_cake(db: Session, id: int):
    cake_returned = db.query(Cake).filter(Cake.id == id).first()
    if not cake_returned:
        raise HTTPException(status_code=404, detail="Cake not found")
    return cake_returned


async def cake_update(db: Session, payload: CakeUpdate):
    cake_returned = await get_one_cake(db, payload.id)
    cake_data = payload.dict(exclude_unset=True)
    for key, value in cake_data.items():
        setattr(cake_returned, key, value)

    db.add(cake_returned)
    db.commit()
    db.refresh(cake_returned)
    return cake_data


async def cake_delete(db: Session, id: int):
    cake_returned = await get_one_cake(db, id)
    db.delete(cake_returned)
    db.commit()
    return True
