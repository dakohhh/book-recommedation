from beanie import PydanticObjectId
from ..database.models import Books
from ..routers.schema.book import CreateBook
from typing import List


class BookRepository:
    @staticmethod
    async def get_all() -> List[Books]:

        pipeline = [
            {"$match": {}},
            {
                "$project": {
                    "_id": 0,
                    "id": {"$toString": "$_id"},
                    "title": 1,
                    "author": 1,
                    "language_code": 1,
                    "genres": 1,
                }
            },

            { "$sort": { "created_at": -1 } }  
        ]

        query = Books.objects.aggregate(*pipeline)

        return query

    @staticmethod
    async def get_by_id(book_id):
        query = Books.objects(id=book_id).first()

        return query

    @staticmethod
    async def create(book: CreateBook):

        query = Books(language_code=book.langauge_code, title=book.title, author=book.author, genres=book.genres)

        query.save()

        return query

    @staticmethod
    async def update(self, book: Books, update_data: CreateBook):

        book.update(**update_data)

        book.save()

        return book

    @staticmethod
    async def delete(book_id: PydanticObjectId):

        query = Books.objects(id=book_id)

        query.delete()

        return query
    
    @staticmethod
    async def delete_all():

        Books.objects().delete()

        return True
