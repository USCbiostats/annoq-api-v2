from src.config.es import es
from src.config.settings import settings
import pytest
import requests

@pytest.mark.asyncio_cooperative
async def test_elasticsearch():
    response = await es.ping()
    assert response == True


@pytest.mark.asyncio_cooperative
async def test_elasticsearch_mappings_count():
    mapping = await es.indices.get_mapping(index=settings.ES_INDEX)
    assert len(list(mapping[settings.ES_INDEX]['mappings']['properties'].keys())) == 533


@pytest.mark.asyncio_cooperative
async def test_elasticsearch_query():
    resp = await es.search(
          index=settings.ES_INDEX,
          query={"match_all": {}},
          size=20,
    )
    assert len(resp['hits']['hits']) == 20


def test_strawberry():
    response = requests.get(settings.API_URL + 'graphql')
    assert response.status_code == 200