from fastapi import FastAPI, Depends
from tortoise.contrib.fastapi import register_tortoise

import db_models
import routers
import schemas
from dependencies import get_current_user

app = FastAPI()


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['db_models']},
    generate_schemas=True,
    add_exception_handlers=True
)


app.include_router(routers.users_router)
app.include_router(routers.auth_router)
app.include_router(routers.exercises_router)


@app.get('/some', response_model=schemas.User)
def something(current_user: db_models.User = Depends(get_current_user)):
    return current_user
