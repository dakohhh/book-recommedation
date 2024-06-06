from mongoengine import Document, StringField, EmailField, ListField


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

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "language_code": self.language_code,
            "genres": self.genres
        }