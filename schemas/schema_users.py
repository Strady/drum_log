import typing
from pydantic import BaseModel


class User(BaseModel):

    id: int
    email: str
    username: typing.Optional[str] = None


class RegistrationData(BaseModel):

    email: str
    username: typing.Optional[str] = None
    password: str
