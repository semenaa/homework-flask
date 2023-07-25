import pydantic
from pydantic import BaseModel, validator
from typing import Optional, Type


class CreateUser(BaseModel):
    name: str
    password: str

    def secure_password(cls, value):
        if len(value) <= 8:
            raise ValueError('Password is too short')
        return value


class UpdateUser(BaseModel):
    name: Optional[str]
    password: Optional[str]

    def secure_password(cls, value):
        if len(value) <= 8:
            raise ValueError('Password is too short')
        return value




