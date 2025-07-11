import os
from dotenv import load_dotenv

load_dotenv()

from databases import Database
from sqlalchemy import (Column,Integer,MetaData,Table,Text,create_engine)

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("username",Text,nullable=False,unique=True),
    Column("email",Text,nullable=False,unique=True),
    Column("password",Text,nullable=False),
    Column("refresh_token",Text)
)

database = Database(DATABASE_URL)