from db_models import User
from tortoise.contrib.pydantic import pydantic_model_creator


UserSchema = pydantic_model_creator(User, name='UserSchema', exclude=('password_hash', 'exercises', 'groups', 'logs'))
_NewUserSchemaBase = pydantic_model_creator(
    User, name='_NewUserSchemaBase', exclude=('password_hash',), exclude_readonly=True
)


class RegistrationData(_NewUserSchemaBase):

    password: str
