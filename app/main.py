from contextlib import asynccontextmanager
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import Request
from starlette.middleware.cors import CORSMiddleware

from src.logic.elastic import ElasticService
from src.logic.embed import EmbeddingService
from src.model.models import SearchSettings, VideoItem

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.embed_srv = EmbeddingService()
    app.state.es = ElasticService(app.state.embed_srv)
    yield
    print('456')


openapi_desc = [
    {
        "name": "Поиск",
        "description": "Поиск видео по текстовому запросу",
    },
    {
        "name": "Предложения",
        "description": "Текстовые предложения запроса",
    },
    {
        "name": "Настройка",
        "description": "Настройка весов поиска"
    }
]

app = FastAPI(lifespan=lifespan, openapi_tags=openapi_desc)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search", tags=['Поиск'])
def video_search(text: str, api: Request) -> List[VideoItem]:
    elastic_service: ElasticService = api.app.state.es
    videos = elastic_service.search_by_text_composite(text)

    def map_to_response_item(video) -> VideoItem:
        resp_item = {
            'link': video['link']
        }
        if 'tags' in video:
            resp_item['description'] = video['tags']
        if 'summary' in video:
            resp_item['short_description'] = video['summary']
        return VideoItem(**resp_item)

    response = list(map(map_to_response_item, videos))
    return response


# @app.put("/videos/settings", tags=['Настройка'])
# def put_search_settings(settings: SearchSettings, api: Request) -> None:
#     elastic_service: ElasticService = api.app.state.es
#     res = elastic_service.set_settings(settings)
#     return res


@app.get("/videos/suggest", tags=['Предложения'])
def suggest(query: str, api: Request) -> List[str]:
    elastic_service: ElasticService = api.app.state.es
    res = elastic_service.suggest(query)
    return res
