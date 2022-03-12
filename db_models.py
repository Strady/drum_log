import typing

from tortoise.models import Model
from tortoise import fields
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
    user = fields.ForeignKeyField('models.User', related_name='exercises')
    group = fields.ForeignKeyField('models.Group', related_name='exercises', null=True)

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
            user=user,
            image_name=image_name,
            description=description,
            group=group
        )
        return result[0]


