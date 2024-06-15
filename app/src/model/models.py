from pydantic import BaseModel


class VideoItem(BaseModel):
    link: str
    description: str = None
    short_description: str = None


class SearchRequest(BaseModel):
    text: str


class SearchSettings(BaseModel):
    description_ru_boost: float
    voice_boost: float
    tags_boost: float
