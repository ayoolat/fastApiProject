from boto3 import Session
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status

from database.database import get_db
from schema.cart import Cart
from schema.response import ResponseDTO
from schema.user import User
from services.auth.dependency import firebase_authentication
from services.cart.cartDto import CartDto
from services.cart.dependency import add_to_user_cart, get_cart, clear_user_cart, mark_user_cart_as_paid, \
    remove_one_cart_item

router = APIRouter(tags=['Cart'])
baseUrl = "api/v1/cart"
userId = "{user_profile_id}"
cartId = "{cart_id}"


@router.post(f"/{baseUrl}/", status_code=status.HTTP_201_CREATED, response_model=ResponseDTO[Cart], )
async def add_to_cart(request: CartDto, db: Session = Depends(get_db),
                      token: User = Depends(firebase_authentication)
                      ):
    response = await add_to_user_cart(request, db)
    return response


@router.get(f"/{baseUrl}", status_code=status.HTTP_200_OK, response_model=ResponseDTO[Cart])
async def get(skip: int, limit: int, db: Session = Depends(get_db),  user: User = Depends(firebase_authentication)):
    response = await get_cart(skip, limit, user.user_id, db)
    return response


@router.delete(f"/{baseUrl}", status_code=status.HTTP_200_OK, response_model=ResponseDTO[bool])
async def clear(user: HTTPAuthorizationCredentials = Depends(firebase_authentication), db: Session = Depends(get_db)):
    response = await clear_user_cart(db, user.id)
    return response


@router.put(f"/{baseUrl}", status_code=status.HTTP_200_OK, response_model=ResponseDTO[bool])
async def mark_as_paid(db: Session = Depends(get_db), user: HTTPAuthorizationCredentials  = Depends(firebase_authentication)):
    response = await mark_user_cart_as_paid(db, user.id)
    return response

@router.delete(f"/{baseUrl}/{cartId}", status_code=status.HTTP_200_OK, response_model=ResponseDTO[bool])
async def remove_item(cart_id: int, db: Session = Depends(get_db), user: HTTPAuthorizationCredentials = Depends(firebase_authentication)):
    response = await remove_one_cart_item(db, cart_id, user.id)
    return response
