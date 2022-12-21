from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from database.database import get_db
from schema.user import User
from services.auth.dependency import logs_in_user, register_user
from services.auth.loginSchema import Login
from services.auth.registerSchema import Register

router = APIRouter(tags=['Auth'])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: Login):
    response = await logs_in_user(request)
    return response


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=User)
async def register(request: Register, db: Session = Depends(get_db)):
    print(request)
    response = await register_user(request, db)
    return response
