from ..database import BaseModel
from .User import User
from peewee import *


class Equipment(BaseModel):
    name = CharField()
    description = CharField()
    available = BooleanField(default=True)
    owner = ForeignKeyField(User, null=True, backref="equipments")
