from elasticsearch import AsyncElasticsearch

from config.settings import settings

es = AsyncElasticsearch(settings.ES_URL,
    maxsize=400,
    timeout=120,
    max_retries=10,
    retry_on_timeout=True)