from boto3 import Session
from fastapi import APIRouter, Depends
from starlette import status

from database.database import get_db
from schema.cart import Cart
from schema.response import ResponseDTO
from services.cart.cartDto import CartDto
from services.cart.dependency import add_to_user_cart, get_cart, clear_user_cart, mark_user_cart_as_paid

router = APIRouter(tags=['Cart'])
baseUrl = "api/v1/cart"
userId = "{user_profile_id}"


@router.post(f"{baseUrl}/", status_code=status.HTTP_201_CREATED, response_model=ResponseDTO[Cart])
async def add_to_cart(request: CartDto, db: Session = Depends(get_db)):
    response = await add_to_user_cart(request, db)
    return response


@router.get(f"{baseUrl}/{userId}", status_code=status.HTTP_200_OK, response_model=ResponseDTO[Cart])
async def get(skip: int, limit: int, user_profile_id: int, db: Session = Depends(get_db)):
    response = await get_cart(skip, limit, user_profile_id, db)
    return response


@router.delete(f"{baseUrl}/{userId}", status_code=status.HTTP_200_OK, response_model=ResponseDTO[bool])
async def clear(user_profile_id: int, db: Session = Depends(get_db)):
    response = await clear_user_cart(db, user_profile_id)
    return response


@router.put(f"{baseUrl}/{userId}", status_code=status.HTTP_200_OK, response_model=ResponseDTO[bool])
async def clear(user_profile_id: int, db: Session = Depends(get_db)):
    response = await mark_user_cart_as_paid(db, user_profile_id)
    return response
