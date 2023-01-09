from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette import status

from database.database import get_db
from schema.response import ResponseDTO
from schema.user import User
from services.auth.dependency import logs_in_user, register_user, get_user, firebase_authentication
from services.auth.loginSchema import Login
from services.auth.registerSchema import Register

router = APIRouter(tags=['Auth'])
baseUrl = "/api/v1/auth"


@router.post(f"{baseUrl}/login", status_code=status.HTTP_200_OK)
async def login(request: Login):
    response = await logs_in_user(request)
    return response


@router.post(f"{baseUrl}/register", status_code=status.HTTP_201_CREATED, response_model=User)
async def register(request: Register, db: Session = Depends(get_db)):
    print(request)
    response = await register_user(request, db)
    return response


@router.get(f"{baseUrl}/", status_code=status.HTTP_200_OK, response_model=ResponseDTO[User])
async def get(db: Session = Depends(get_db),
              user: User = Depends(firebase_authentication)
              ):
    response = await get_user(user.user_id, db)
    return response
