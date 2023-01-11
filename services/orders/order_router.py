from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from database.database import get_db
from schema.cart import Cart
from schema.response import ResponseDTO
from schema.user import User
from services.auth.dependency import firebase_authentication
from services.cart.dependency import get_all_cart_items, get_all_completed_orders

router = APIRouter(tags=['Orders'])
baseUrl = "api/v1/orders"


@router.get(f"/{baseUrl}", status_code=status.HTTP_200_OK, response_model=ResponseDTO[Cart])
async def get_all_orders(skip: int, limit: int, db: Session = Depends(get_db),  user: User = Depends(firebase_authentication)):
    response = await get_all_cart_items(skip, limit, user.id, db)
    return response


@router.get(f"/{baseUrl}/completed", status_code=status.HTTP_200_OK, response_model=ResponseDTO[Cart])
async def get_completed_orders(skip: int, limit: int, db: Session = Depends(get_db),  user: User = Depends(firebase_authentication)):
    response = await get_all_completed_orders(db, skip, limit, user.id)
    return response
