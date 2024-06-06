from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from .settings import settings
from .routers import auth, book
import pandas as pd
from .database.models import Books
from .database import connect_to_mongo, disconnect_from_mongo


app = FastAPI(title=settings.APP_NAME, version="0.1.0")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": False,
            "message": exc.detail,
            "data": getattr(exc, "data", None),
        },
    )


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
    await disconnect_from_mongo()


app.include_router(auth)
app.include_router(book)


@app.get("/")
async def root(requeest: Request):

    return {"setting": settings.APP_NAME}


@app.get("/hjg")
async def add_books():

    def split_with_comma(value:list):

        new_list = []

        for i in range(len(value)):

            if "," in value[i]:
                temp_value = value[i]

                new_list.extend(temp_value.split(","))

            else:
                new_list.append(value[i])

        return new_list


    data = pd.read_csv("./book_with_genre_dataset.csv")

    data = data.dropna(subset=['genres'])

    data["genres"] = data["genres"].str.split(";")

    data["genres"] = data["genres"].apply(split_with_comma)


    for index, row in data.iterrows():
        title = row[1]
        author = row[2]
        language_code = row[6]
        genres = row[12]

        new_book = Books(title=title, author=author, genres=genres, language_code=language_code)

        new_book.save()


    return True

