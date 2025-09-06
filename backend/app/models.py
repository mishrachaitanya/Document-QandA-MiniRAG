from pydantic import BaseModel
from typing import List


class AskRequest(BaseModel):
    query: str
    top_k: int = 4


class AskResponse(BaseModel):
    answer: str
    sources: List[dict]