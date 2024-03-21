from src.config.es import es
from src.config.settings import settings
import pytest

@pytest.mark.asyncio_cooperative
async def test_elasticsearch():
    response = await es.ping()
    assert response == True


@pytest.mark.asyncio_cooperative
async def test_elasticsearch_mappings_count():
    mapping = await es.indices.get_mapping(index=settings.ES_INDEX)
    assert len(list(mapping[settings.ES_INDEX]['mappings']['properties'].keys())) == 533