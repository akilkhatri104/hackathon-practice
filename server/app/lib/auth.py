import os
from jose import jwt
from dotenv import load_dotenv
from ..db import database,users
from sqlalchemy import update
load_dotenv()

ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
REFRESH_TOKEN_SECRET = os.environ.get("REFRESH_TOKEN_SECRET")
async def create_session(user_id: int):
    try:
        await database.connect()
        print("Creating session for user_id:", user_id)
        access_token = jwt.encode({'user_id': str(user_id)},ACCESS_TOKEN_SECRET,"HS256")
        print("Access token:", access_token)
        refresh_token = jwt.encode({'user_id': str(user_id)},REFRESH_TOKEN_SECRET,"HS256")

        print("Updating refresh token in database")
        stmt = update(users).where(users.c.id == user_id).values(refresh_token=refresh_token)
        update_result = await database.execute(stmt)

        print("Returning access token")
        return access_token
    except Exception as e:
        print("Exception occured while creating session:", e)
        return None
    finally:
        print("Disconnecting database")
        await database.disconnect()


async def verify_jwt(token: str):
    try:
        await database.connect()
        payload = jwt.decode(token,ACCESS_TOKEN_SECRET,"HS256")
        print(payload['user_id'])
        user_id = int(payload['user_id'])
        query = users.select().where(users.c.id == user_id)
        user_exists = await database.fetch_one(query=query)

        if(user_exists == None):
            return None
        return user_id
    except Exception as e:
        print(e)
        return None
    finally: 
        await database.disconnect()




async def delete_refresh_token_from_db(user_id:int):
    try:
        print("Deleting refresh token for user_id:", user_id)
        await database.connect()
        

        stmt = update(users).where(users.c.id == user_id).values(refresh_token=None)
        print("Deleting refresh token with query:", stmt)
        update_result = await database.execute(stmt)

        print("Refresh token deleted successfully")
        return True
    except Exception as e:
        print("Exception occured while deleting refresh token:", e)
        return False
    finally:
        print("Disconnecting database")
        await database.disconnect()
