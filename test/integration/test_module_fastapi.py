from fastapi.testclient import TestClient
from src.main import app
from src.config.settings import settings
from src.routers import snp
import json

client = TestClient(app)


def expected_version():
    with open('./data/anno_tree.json') as f:
        chr_version = next(elt["version"] for elt in json.load(f) if elt["name"] == "chr")
    return {
        "api_version": snp.VERSION,
        "data_version": chr_version,
        "genome_build": settings.ANNOQ_GENOME_BUILD,
        "dbsnp_release": settings.ANNOQ_DBSNP_RELEASE,
        "wgsa_version": settings.ANNOQ_WGSA_VERSION,
    }


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == expected_version()


def test_read_annotations():
    response = client.get("/annotations")
    assert response.status_code == 200
    with open('./data/api_mapping_anno_tree.json') as f:
        data = json.load(f)
        assert response.json() == data


def test_read_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == expected_version()

