from fastapi import APIRouter, Request
from .schema.book import CreateBook
from ..database.models import Books

router = APIRouter()


@router.get("/book")
async def book():
    return {"message": "Book"}


@router.post("/book")
async def add_book(request: Request, create_book: CreateBook):

    new_book = Books(**create_book.model_dump())
    new_book.save()
    return new_book.to_dict()
