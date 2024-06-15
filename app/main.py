from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import Request
from starlette.middleware.cors import CORSMiddleware

from src.logic.elastic import ElasticService
from src.logic.embed import EmbeddingService
from src.model.models import SearchSettings

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


@app.get("/search")
def video_search(text: str, api: Request):
    elastic_service: ElasticService = api.app.state.es
    videos = elastic_service.search_by_text_composite(text)

    def map_to_response_item(video):
        resp_item = {
            'link': video['link']
        }

        if 'tags' in video:
            resp_item['description'] = video['tags']
        if 'summary' in video:
            resp_item['short_description'] = video['summary']

        return resp_item

    response = list(map(map_to_response_item, videos))
    return response


@app.put("/videos/settings")
def video_search(settings: SearchSettings, api: Request):
    elastic_service: ElasticService = api.app.state.es
    res = elastic_service.set_settings(settings)
    return res


@app.get("/videos/suggest")
def get_video_search(query: str, api: Request):
    elastic_service: ElasticService = api.app.state.es
    res = elastic_service.suggest(query)
    return res
