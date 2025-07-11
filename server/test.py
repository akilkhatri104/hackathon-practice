from app.db import database,users
import asyncio
from sqlalchemy import select

async def main():
    await database.connect()
    query = users.select().where(users.c.id == 1)
    results = await database.fetch_one(query=query)
    print(results["username"])
    await database.disconnect()

asyncio.run(main())

