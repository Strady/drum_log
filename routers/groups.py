from fastapi import APIRouter, HTTPException, status
import db_models
import schemas
import settings

app_config = settings.AppSettings()

router = APIRouter(prefix='/groups', tags=["groups"])


@router.get('/groups', response_model=list[schemas.Group])
async def get_groups():

    return await db_models.Group.all()


@router.post('/group', response_model=schemas.Group)
async def create_group(new_group: schemas.NewGroup):
    user = await db_models.User.get_or_none(id=new_group.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with ID {new_group.user_id} does not exist'
        )
    return await db_models.Group.add(name=new_group.name, user=user)

