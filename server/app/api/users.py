from fastapi import APIRouter, HTTPException
from typing import List

from .crud import create_new_user, get_user_by_id, get_all_users, update_user, delete_user
from .models import User, UserCreate, UserUpdate
from ..db import database

userRouter = APIRouter()

@userRouter.post('/user', response_model=User)
async def post_user(user: UserCreate):
    await database.connect()
    result = await create_new_user(user=user)
    await database.disconnect()
    return result

@userRouter.get('/user/{user_id}', response_model=User)
async def get_user(user_id: int):
    await database.connect()
    user = await get_user_by_id(user_id)
    await database.disconnect()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@userRouter.get('/users', response_model=List[User])
async def get_users():
    await database.connect()
    users = await get_all_users()
    await database.disconnect()
    return users

@userRouter.put('/user/{user_id}', response_model=User)
async def put_user(user_id: int, user: UserUpdate):
    await database.connect()
    updated_user = await update_user(user_id, user)
    await database.disconnect()
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@userRouter.delete('/user/{user_id}')
async def delete_user_route(user_id: int):
    await database.connect()
    result = await delete_user(user_id)
    await database.disconnect()
    return result