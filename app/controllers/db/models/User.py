import datetime
from peewee import *
from ..database import BaseModel
import uuid
import secrets


def generate_expirity_date() -> datetime:
    current_time = datetime.datetime.now()
    today_plus_month = current_time + datetime.timedelta(days=30)
    return today_plus_month


class User(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField()
    email = CharField(unique=True)
    password_hash = CharField()


class AuthToken(BaseModel):
    token = CharField(unique=True, index=True, default=secrets.token_hex)
    user = ForeignKeyField(User, backref='tokens')
    created_at = DateTimeField(default=datetime.datetime.now)
    expirity_date = DateTimeField(default=generate_expirity_date)
