from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import Request
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from src.logic.elastic import ElasticService
from src.logic.embed import EmbeddingService
from src.model.models import SearchRequest, SearchSettings

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.embed_srv = EmbeddingService()
    app.state.es = ElasticService(app.state.embed_srv)
    yield
    print('456')


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/videos:search")
def video_search(request: SearchRequest, api: Request):
    elastic_service: ElasticService = api.app.state.es
    res = elastic_service.search(request)
    return res


@app.get("/videos")
def get_video_search(query: str, api: Request):
    # elastic_service: ElasticService = api.app.state.es
    # res = elastic_service.search_by_text(query)
    # return res
    elastic_service: ElasticService = api.app.state.es
    res = elastic_service.search_by_text_composite(query)
    return res


@app.get("/videos/mock")
def get_video_search(query: str, api: Request):
    elastic_service: ElasticService = api.app.state.es
    res = elastic_service.search_by_text_mock(query)
    return res


@app.get("/videos/with_voice")
def get_video_search(query: str, api: Request):
    elastic_service: ElasticService = api.app.state.es
    res = elastic_service.search_by_text_with_voice(query)
    return res

@app.get("/videos/composite")
def get_video_search(query: str, api: Request):
    elastic_service: ElasticService = api.app.state.es
    res = elastic_service.search_by_text_composite(query)
    return res

@app.post("/videos/settings")
def video_search(settings: SearchSettings, api: Request):
    elastic_service: ElasticService = api.app.state.es
    res = elastic_service.set_settings(settings)
    return res
