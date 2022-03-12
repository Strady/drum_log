import typing

from fastapi import Depends, HTTPException, status, Body
from jose import jwt, JWTError

import db_models
import schemas
import settings
from schemas.schema_auth import oauth2_scheme


app_settings = settings.AppSettings()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> db_models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, app_settings.jwt_secret, algorithms=['HS256'])
        user_id: typing.Optional[str] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user: typing.Optional[db_models.User] = await db_models.User.get_or_none(id=int(user_id))
    if user is None:
        raise credentials_exception
    return user
