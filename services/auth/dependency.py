from typing import Any, Coroutine

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
from googleapiclient.errors import HttpError
from sqlalchemy.orm import Session

from schema.user import User
from services.auth.loginSchema import Login
from services.auth.registerSchema import Register
from database.database import get_db
from repositories.user import create, get_by_user_id

import pyrebase
import json

from services.respond import Respond

pb = pyrebase.initialize_app(json.load(open("./firebase-config.json")))


async def register_user(user_registration: Register, db: Session = Depends(get_db)):
    try:
        new_user = auth.create_user(email=user_registration.email, password=user_registration.password)
        user = User(email=user_registration.email, first_name=user_registration.first_name,
                    last_name=user_registration.last_name, user_id=new_user.uid)
        user = await create(user, db)
        return user
    except Exception as e:
        raise HTTPException(detail=e.__str__(), status_code=400)


async def logs_in_user(login_payload: Login):
    try:
        login_user = pb.auth().sign_in_with_email_and_password(login_payload.email, login_payload.password)
        return login_user
    except Exception as e:
        raise HTTPException(detail=e.__str__(), status_code=400)


async def get_user(user_id: str, db: Session):
    user = get_by_user_id(user_id, db)
    respond = Respond[User]()
    return respond.response(
        body=user,
        code=200,
        message="User query successfully"
    )


def firebase_authentication(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
                                  , db: Session = Depends(get_db)
                                ) -> Coroutine[Any, Any, Any]:
    try:
        user = pb.auth().get_account_info(token.credentials)
        db_user = get_by_user_id(user.get("users")[0].get("localId"), db)
        return db_user
    except:
        raise HTTPException(detail="Invalid token", status_code=401)
