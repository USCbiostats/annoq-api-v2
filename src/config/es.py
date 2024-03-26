from elasticsearch import AsyncElasticsearch

from src.config.settings import settings

es = AsyncElasticsearch(settings.ES_URL,
    connections_per_node=400,
    request_timeout=120,
    max_retries=10,
    retry_on_timeout=True)