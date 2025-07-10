from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.users import userRouter
from app.db import database

app = FastAPI()

app.include_router(router=userRouter)


