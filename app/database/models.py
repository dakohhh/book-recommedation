from mongoengine import Document, StringField, EmailField, ListField, DateTimeField
from datetime import datetime


class User(Document):
    first_name = StringField()
    last_name = StringField()
    email = EmailField()
    password = StringField()


class Books(Document):
    title = StringField()
    author = StringField()
    language_code = StringField()
    genres = ListField()
    created_at = DateTimeField(default=datetime.now)

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "language_code": self.language_code,
            "genres": self.genres
        }