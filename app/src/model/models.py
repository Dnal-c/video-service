from typing import List, Any

from paprika import *
from pydantic import BaseModel


@data
class Video:
    video_url: str
    title: str
    tags: List[str]
    summary: str


class SearchRequest(BaseModel):
    text: str


class SearchSettings(BaseModel):
    description_ru_boost: float
    voice_boost: float
    tags_boost: float


