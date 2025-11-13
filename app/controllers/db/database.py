from peewee import Model, SqliteDatabase


db = SqliteDatabase('reserve.db')


class BaseModel(Model):
    class Meta:
        database = db
