from pydantic import BaseModel
from typing import List


class CreateBook(BaseModel):
    title: str
    author: str
    langauge_code: str
    genres: List[str]
