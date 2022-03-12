import typing
from datetime import datetime

from pydantic import BaseModel, Field


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


class ExerciseLog(BaseModel):
    id: int
    date_time: datetime
    bpm: int = Field(..., gt=0)
    user_id: int
    exercise_id: int

    class Config:
        orm_mode = True


class NewExerciseLog(BaseModel):
    bpm: int = Field(..., gt=0)
    user_id: int
    exercise_id: int

    class Config:
        orm_mode = True


