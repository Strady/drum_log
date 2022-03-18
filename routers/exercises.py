import os
import typing
import aiofiles
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Body, Form
import db_models
import schemas
import settings

app_config = settings.AppSettings()

router = APIRouter(prefix='/exercises', tags=["exercises"])


@router.post('/exercise', response_model=schemas.Exercise)
async def create_exercise(name: str = Form(...),
                          description: typing.Optional[str] = Form(None),
                          user_id: int = Form(...),
                          group_id: typing.Optional[int] = Form(None),
                          file: typing.Optional[UploadFile] = File(None)
                          ):
    user = await db_models.User.get_or_none(id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with ID {user_id} does not exist'
        )

    group = None
    if group_id is not None:
        group = await db_models.Group.get_or_none(id=group_id)
        if group is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Group with ID {group_id} does not exist'
            )

    exercise = await db_models.Exercise.add(
        name=name,
        user=user,
        image_name=file.filename if file else None,
        description=description,
        group=group
    )

    if file:
        picture_name = os.path.join(os.getcwd(), app_config.images_dir, f'{exercise.id}_{file.filename}')
        content = await file.read()
        async with aiofiles.open(picture_name, 'wb') as f:
            await f.write(content)

    return exercise

@router.get('/exercises', response_model=list[schemas.Exercise])
async def get_exercises():
    return await db_models.Exercise.all()

# TODO implement deletion and updating for exercises


@router.post('/exercise_logs', response_model=schemas.ExerciseLog)
async def create_exercise_log(new_log: schemas.NewExerciseLog):
    user = await db_models.User.get_or_none(id=new_log.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with ID {new_log.user_id} does not exist'
        )

    exercise = await db_models.Exercise.get_or_none(id=new_log.exercise_id)
    if exercise is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Exercise with ID {new_log.exercise_id} does not exist'
        )

    return await db_models.ExerciseLog.add(bpm=new_log.bpm, user=user, exercise=exercise)


@router.get('/exercise_logs', response_model=list[schemas.ExerciseLog])
async def get_exercise_logs():
    return await db_models.ExerciseLog.all()
