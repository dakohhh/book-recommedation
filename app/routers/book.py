from fastapi import APIRouter, Request
from .schema.book import CreateBook
from ..client.response import CustomResponse
from ..utils.exceptions import BadRequestException
from ..repository import BookRepository
router = APIRouter()


@router.get("/book")
async def book():

    books = await BookRepository().get_all()

    context = {"books": list(books)}

    return CustomResponse("all books", data=context)



@router.post("/book")
async def add_book(request: Request, create_book: CreateBook):

    book = await BookRepository().create(create_book)

    context = {"book": book.to_dict()}
    return CustomResponse("created book successfully", data=context)



@router.delete("/book")
async def delete_all_books(request: Request):

    await BookRepository().delete_all()

    return CustomResponse("All books deleted successfully")