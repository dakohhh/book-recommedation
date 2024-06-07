from pydantic import BaseModel
from typing import List

class GetBookRecommendation(BaseModel):
    genres: List[str]
    language_code: str
