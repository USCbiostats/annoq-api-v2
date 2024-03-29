from src.config.es import es
from src.config.settings import settings
import pytest
import json
from src.graphql.models.snp_model import Snp

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


def test_generator_attribute():
    snps = Snp()
    assert hasattr(snps, 'chr')
    assert hasattr(snps, 'pos')
    assert hasattr(snps, 'ref')
    # assert hasattr(snps, 'SnpEff_ensembl_CDS_position_CDS_len')


def test_class_schema():
    with open("./scripts/class_generators/class_schema.json") as f:
        data = json.load(f)
        assert data['title'] == "Snp"
        assert data['properties']['chr'] == {"type": "model.Annotation"}
        assert data['properties']['_1000Gp3_AC'] == {"type": "model.Annotation"}
