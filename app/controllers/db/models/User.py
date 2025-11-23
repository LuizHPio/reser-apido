import datetime
from peewee import *
from ..database import BaseModel
import uuid
from typing import TypeVar, Literal

REFRESH_TOKEN_MAXAGE_MINUTES = 60 * 24 * 30  # 30 dias
roles: TypeVar = ["admin", "user"]


def generate_expiry_date(max_age=None) -> datetime.datetime:
    time_to_add = 0
    if max_age == None:
        time_to_add = REFRESH_TOKEN_MAXAGE_MINUTES
    else:
        time_to_add = max_age

    current_time = datetime.datetime.now()
    today_plus_expiry = current_time + \
        datetime.timedelta(minutes=time_to_add)
    return today_plus_expiry


class User(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    role = CharField(default="user")
    name = CharField()
    email = CharField(unique=True)
    password_hash = CharField()


class RefreshToken(BaseModel):
    family = UUIDField()
    user = ForeignKeyField(User, backref='tokens')
    created_at = DateTimeField(default=datetime.datetime.now)
    expiry_date = DateTimeField(default=generate_expiry_date)
    is_used = BooleanField(default=False)
