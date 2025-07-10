from ..db import database,users
from .models import User
import bcrypt

async def create_new_user(user: User):
    print("create_new_user: ",user)
    bytes = user.password.encode('utf-8')
    hashedPassword = bcrypt.hashpw(bytes,bcrypt.gensalt()).decode('utf-8')
    
    query = users.insert().values(id=user.id,username = user.username,email= user.email,password=hashedPassword)
    result = await database.execute(query=query)
    return result

    