from fastapi import HTTPException
from pydantic import BaseModel, root_validator, ValidationError


class PasswordBase(BaseModel):
    password: str
    confirm_password: str

    @root_validator()
    def validate_password_model(cls, value):
        password = value.get("password")
        confirm_password = value.get("confirm_password")
        if password != confirm_password:
            raise HTTPException(status_code=400, detail='passwords do not match')
        if len(password) < 8:
            print(len(password))
            raise HTTPException(status_code=400, detail='Password must be at least 8 characters long.')
        if not any(character.isupper() for character in password):
            raise HTTPException(status_code=400, detail='Password should contain at least one upperCase character.')
        return value

    class Config:
        orm_mode = True
