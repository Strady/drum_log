from fastapi import APIRouter
from passlib.hash import bcrypt
import db_models
import schemas

router = APIRouter(prefix='/users', tags=["users"])


@router.get('/', response_model=list[schemas.UserSchema])
async def get_users():
    return await schemas.UserSchema.from_queryset(db_models.User.all())


@router.post('/', response_model=schemas.UserSchema, response_model_exclude={'password_hash'})
async def create_user(user_data: schemas.RegistrationData):
    return await db_models.User.create(
        email=user_data.email,
        username=user_data.username,
        password_hash=bcrypt.hash(user_data.password)
    )

