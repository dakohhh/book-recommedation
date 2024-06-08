from fastapi import APIRouter, Request
from bson import ObjectId

from app.database.models import Books
from .schema.recommend import GetBookRecommendation
from ..client.response import CustomResponse
from ..repository import BookRepository

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors


router = APIRouter(tags=["Recommendation"], prefix="/recommnend")


def encode_language_code_values(value: str):

    codes = {
        "eng": 1,
        "en-US": 2,
        "fre": 3,
        "spa": 4,
        "en-GB": 5,
        "mul": 6,
        "grc": 7,
        "enm": 8,
        "en-CA": 9,
        "ger": 10,
        "jpn": 11,
        "ara": 12,
        "nl": 13,
        "zho": 14,
        "lat": 15,
        "por": 15,
        "ita": 16,
        "rus": 17,
        "msa": 18,
        "glg": 19,
        "swe": 20,
        "nor": 21,
        "tur": 22,
        "gla": 23,
        "ale": 24,
    }
    return codes[value]


@router.post("/")
async def recommend_book(request: Request, recommend: GetBookRecommendation):
    books = await BookRepository().get_all()

    data = pd.DataFrame(list(books))

    data.drop(["author", "title"], axis=1, inplace=True)

    unique_genres = set()

    for genres in data["genres"]:
        unique_genres.update(genres)

    for genre in unique_genres:
        data[genre] = data["genres"].apply(lambda x: 1 if genre in x else 0)

    data["language_code"] = data["language_code"].apply(encode_language_code_values)

    data.drop("genres", axis=1, inplace=True)

    preprocessed_data = data.copy()

    preprocessed_data.set_index("id", inplace=True)

    user_input_array = []

    user_input_array.append(encode_language_code_values(recommend.language_code))

    for col in preprocessed_data.columns[1:]:
        if col in recommend.genres:
            user_input_array.append(1)
        else:
            user_input_array.append(0)

    user_input_array = np.array(user_input_array).reshape(1, -1)

    print(user_input_array)

    nn_model = NearestNeighbors(metric="minkowski", radius=0.5, p=2)

    nn_model.fit(preprocessed_data)

    distances, neighbors = nn_model.kneighbors(user_input_array, n_neighbors=10)

    ids_to_fetch = []

    for index in neighbors[0]:
        ids_to_fetch.append(ObjectId(data.iloc[index]["id"]))

    pipeline = [
        {"$match": {"_id": {"$in": ids_to_fetch}}},
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
    ]

    # Using the aggregate method to execute the pipeline
    result = Books.objects.aggregate(*pipeline)

    context = {"recommendations": list(result)}

    return CustomResponse("Recommendations for genres", data=context)
