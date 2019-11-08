import peewee as pw

from models.base_model import BaseModel


class User(BaseModel):
    full_name = pw.CharField()
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()
