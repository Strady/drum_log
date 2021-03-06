import typing

from tortoise.models import Model
from tortoise import fields, Tortoise
from passlib.hash import bcrypt


class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(255, unique=True)
    username = fields.CharField(50, unique=True, null=True)
    password_hash = fields.CharField(255)

    def verify_password(self, password) -> bool:
        return bcrypt.verify(password, self.password_hash)


class Group(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(100)
    user = fields.ForeignKeyField('models.User', related_name='groups')

    @classmethod
    async def add(cls, name: str, user: User):
        result = await Group.get_or_create(
            name=name,
            user=user
        )
        return result[0]


class Exercise(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(100)
    image_name = fields.CharField(100, null=True)
    description = fields.TextField(null=True)
    users: fields.ManyToManyRelation['User'] = fields.ManyToManyField(
        'models.User', related_name='exercises', through='exercise_user'
    )
    groups: fields.ManyToManyRelation['Group'] = fields.ManyToManyField(
        'models.Group', related_name='exercises', through='exercise_group'
    )

    @classmethod
    async def add(cls,
                  name: str,
                  user: User,
                  image_name: typing.Optional[str] = None,
                  description: typing.Optional[str] = None,
                  group: typing.Optional[Group] = None
                  ):
        result = await Exercise.get_or_create(
            name=name,
            image_name=image_name,
            description=description,
        )
        exercise = result[0]
        await exercise.users.add(user)
        if group:
            await exercise.groups.add(group)
        return result[0]


class ExerciseLog(Model):
    id = fields.IntField(pk=True)
    date_time = fields.DatetimeField(auto_now_add=True)
    bpm = fields.IntField()
    user = fields.ForeignKeyField('models.User', related_name='logs')
    exercise = fields.ForeignKeyField('models.Exercise', related_name='logs')

    @classmethod
    async def add(cls, bpm: int, user: User, exercise: Exercise):
        result = await ExerciseLog.get_or_create(bpm=bpm, user=user, exercise=exercise)
        return result[0]


Tortoise.init_models(['db_models'], 'models')


