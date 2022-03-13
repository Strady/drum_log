from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import routers

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

