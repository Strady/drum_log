import typing

from pydantic import BaseModel


class Group(BaseModel):

    id: int
    name: str
    user_id: int

    class Config:
        orm_mode = True


class NewGroup(BaseModel):

    name: str
    user_id: int

    class Config:
        orm_mode = True


class Exercise(BaseModel):
    id: int
    name: str
    image_name: typing.Optional[str]
    description: typing.Optional[str]
    user_id: int
    group_id: typing.Optional[int]

    class Config:
        orm_mode = True


class NewExercise(BaseModel):
    name: str
    image_name: typing.Optional[str]
    description: typing.Optional[str]
    user_id: int
    group_id: typing.Optional[int]

    class Config:
        orm_mode = True


