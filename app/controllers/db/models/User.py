import datetime
from peewee import *
from ..database import BaseModel
import uuid
import secrets


class User(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField()
    email = CharField(unique=True)
    password_hash = CharField()


class AuthToken(BaseModel):
    token = CharField(unique=True, index=True, default=secrets.token_hex)
    user = ForeignKeyField(User, backref='tokens')
    created_at = DateTimeField(default=datetime.datetime.now)
