from ..db import database,users
from .models import User, UserCreate, UserUpdate
import bcrypt
from sqlalchemy import select

async def create_new_user(user: UserCreate):
    print("create_new_user: ",user)
    bytes = user.password.encode('utf-8')
    hashedPassword = bcrypt.hashpw(bytes,bcrypt.gensalt()).decode('utf-8')
    query = users.insert().values(username = user.username,email= user.email,password=hashedPassword)
    result = await database.execute(query=query)
    return {"id": result, **user.dict(exclude={'password'})}

async def get_user_by_id(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)

async def get_all_users():
    query = users.select()
    return await database.fetch_all(query)

async def update_user(user_id: int, user: UserUpdate):
    values = user.dict(exclude_unset=True)
    if 'password' in values:
        values['password'] = bcrypt.hashpw(values['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    query = users.update().where(users.c.id == user_id).values(**values)
    await database.execute(query)
    return await get_user_by_id(user_id)

async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {"message": f"User {user_id} deleted"}

