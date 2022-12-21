from pydantic import BaseModel, EmailStr

from services.auth.passwordSchema import PasswordBase


class Register(PasswordBase):
    first_name: str
    last_name: str
    email: EmailStr
