import os.path

import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import routers
import settings

app_config = settings.AppSettings()

app = FastAPI()


app.include_router(routers.users_router)
app.include_router(routers.auth_router)
app.include_router(routers.exercises_router)
app.include_router(routers.groups_router)
app.include_router(routers.exercise_logs_router)


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


if __name__ == '__main__':

    pictures_dir = os.path.join(os.getcwd(), app_config.images_dir)
    if not os.path.exists(pictures_dir):
        os.makedirs(pictures_dir)

    register_tortoise(
        app,
        db_url='sqlite://db.sqlite3',
        modules={'models': ['db_models']},
        generate_schemas=True,
        add_exception_handlers=True
    )
    uvicorn.run(app, host="0.0.0.0", port=8000)


