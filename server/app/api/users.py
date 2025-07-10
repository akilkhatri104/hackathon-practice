from fastapi import APIRouter

from .crud import create_new_user
from .models import User
from ..db import database

userRouter = APIRouter()

@userRouter.post('/user')
async def post_user(user: User):
    await database.connect()
    result = await create_new_user(user=user)
    await database.disconnect()
    return result