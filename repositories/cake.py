from sqlalchemy.orm import Session

import schema


async def add_cake(payload: schema.cake.Cake, db: Session):
    return ""