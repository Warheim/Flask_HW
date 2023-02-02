import re
from pydantic import BaseModel, EmailStr, ValidationError, validator
from typing import Optional, Type
from errors import HttpException

PASSWORD_REGEX = re.compile("^(?=.*[a-z_])(?=.*\d)(?=.*[@$!%*#?&_])[A-Za-z\d@$!#%*?&_]{8,20}$")


def check_password(password: str):
    if len(password) > 20:
        raise ValueError('max length password is 20')
    if not re.search(PASSWORD_REGEX, password):
        raise ValueError('password is too easy')
    return password


class CreateUserValidator(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def strong_password(cls, value):
        return check_password(value)


class PatchUserValidator(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]

    @validator('password')
    def strong_password(cls, value):
        return check_password(value)


class CreateAdvValidator(BaseModel):
    title: str
    description: Optional[str]


class PatchAdvValidator(BaseModel):
    title: Optional[str]
    description: Optional[str]


VALID_MODEL = Type[CreateUserValidator] | Type[PatchUserValidator] | Type[CreateAdvValidator] | Type[PatchAdvValidator]


def validate(data: dict, valid_model: VALID_MODEL):
    try:
        return valid_model(**data).dict(exclude_none=True)
    except ValidationError as error:
        raise HttpException(400, error.errors())
