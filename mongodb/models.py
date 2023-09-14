from datetime import datetime

from mongoengine import Document
from mongoengine.fields import BooleanField, DateTimeField, StringField, IntField


class Recruiter(Document):
    recr_id = IntField(required=True, unique=True)
    name = StringField(max_length=100)
    link = StringField(max_length=300, unique=True)
    created = DateTimeField(default=datetime.now())
    connection = BooleanField(default=False)
    reply = BooleanField(default=False)
    reason = StringField(max_length=200, default="")
