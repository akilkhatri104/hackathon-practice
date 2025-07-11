from ..db import database,users
from .models import UserRequest

async def create_user(user: UserRequest):
    await database.connect()
    query = users.insert().values(username = user.username,email= user.email,password=user.password)
    result = await database.execute(query=query)
    await database.disconnect()
    return result

    