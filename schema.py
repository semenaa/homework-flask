from typing import Optional, Type

import pydantic
from pydantic import BaseModel, validator


class CreateUser(BaseModel):
    email: str
    password: str

    def secure_password(cls, value):
        if len(value) <= 8:
            raise ValueError('Password is too short')
        return value


class UpdateUser(BaseModel):
    email: Optional[str]
    password: Optional[str]

    def secure_password(cls, value):
        if len(value) <= 8:
            raise ValueError('Password is too short')
        return value


class CreateAd(BaseModel):
    title: str
    description: str



