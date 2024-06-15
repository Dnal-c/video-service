import os

from elasticsearch import Elasticsearch

from app.src.logic.embed import EmbeddingService
from app.src.model.models import SearchSettings


class ElasticService:

    def __init__(self, embed_srv: EmbeddingService):
        settings = {
            'description_ru_boost': 1,
            'voice_boost': 1,
            'tags_boost': 1
        }
        self.search_settings = SearchSettings(**settings)
        host = os.environ['ELASTIC_HOST']
        login = os.environ['ELASTIC_LOGIN']
        password = os.environ['ELASTIC_PASSWORD']
        print(f'ElasticService host: {host}')
        self.es = Elasticsearch(host, basic_auth=(login, password))
        self.index = 'video-index'
        self.embed_service = embed_srv

    def search_by_text_composite(self, text):
        text_vector = self.embed_service.calc(text)
        settings: SearchSettings = self.search_settings
        multi_query = {
            "knn": [
                {
                    "field": "description_ru_vector",
                    "query_vector": text_vector,
                    "k": 10,
                    "boost": settings.description_ru_boost
                },
                {
                    "field": "tags_vector",
                    "query_vector": text_vector,
                    "k": 10,
                    "boost": settings.tags_boost
                },
                {
                    "field": "voice_vector",
                    "query_vector": text_vector,
                    "k": 10,
                    "boost": settings.voice_boost
                }
            ],
            '_source': {
                'includes': ['link', 'description_ru', 'tags', 'summary'],
            }
        }
        response = self.es.search(index=self.index, body=multi_query)
        items = response['hits']['hits']
        return list(map(lambda item: item['_source'], items))

    def set_settings(self, settings: SearchSettings):
        self.search_settings = settings

    def suggest(self, text: str):
        suggest_query = {
            "suggest": {
                "my-suggestion": {
                    "prefix": text,
                    "completion": {
                        "field": "summary.sug",
                        "size": 10,
                        "skip_duplicates": 'true',
                        "fuzzy": {
                            "fuzziness": "AUTO"
                        }
                    }
                }
            },
            "_source": 'false'
        }
        response = self.es.search(index=self.index, body=suggest_query)
        print(response)
        items = list(map(lambda item: item['text'], response['suggest']['my-suggestion'][0]['options']))
        return items
