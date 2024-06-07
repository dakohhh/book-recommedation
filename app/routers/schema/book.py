from pydantic import BaseModel
from typing import List


class CreateBook(BaseModel):
    title: str
    author: str
    language_code: str
    genres: List[str]
