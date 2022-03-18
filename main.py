import os.path

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import routers
import settings

app_config = settings.AppSettings()

pictures_dir = os.path.join(os.getcwd(), app_config.images_dir)
if not os.path.exists(pictures_dir):
    os.makedirs(pictures_dir)

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
app.include_router(routers.groups_router)


