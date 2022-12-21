from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

import schema.user
from database.models.user import User


async def create(payload: schema.user.User, db: Session):
    new_user = User(email=payload.email, first_name=payload.first_name,
                    last_name=payload.last_name, user_id=payload.user_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def get_by_email(email: str, db: Session):
    user = await db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user
