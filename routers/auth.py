import typing
from datetime import datetime, timedelta

from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

import db_models
import settings
from schemas.schema_auth import oauth2_scheme

app_settings = settings.AppSettings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix='/auth', tags=["authentication"])


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db_models.User.get_or_none(email=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'User with {form_data.username} email is not registered',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    if not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Password is incorrect',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    token = jwt.encode(
        claims={'sub': str(user.id), 'exp': datetime.utcnow() + timedelta(app_settings.jwt_ttl)},
        key=app_settings.jwt_secret,
        algorithm='HS256'
    )
    return {'access_token': token, 'token_type': 'bearer'}



