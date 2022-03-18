from fastapi import APIRouter, HTTPException, status
import db_models
import schemas


router = APIRouter(prefix='/exercise_logs', tags=["exercise logs"])


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