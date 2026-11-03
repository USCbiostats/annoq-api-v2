import requests
from src.config.settings import settings
import json

def test_root():
    response = requests.get(settings.SITE_URL)
    assert response.status_code == 200
    version = requests.get(settings.SITE_URL + "version")
    assert version.status_code == 200
    assert response.json() == version.json()


def test_annotations():
    response = requests.get(settings.SITE_URL + "annotations")
    assert response.status_code == 200
    with open('./data/api_mapping_anno_tree.json') as f:
        data = json.load(f)
        assert response.json() == data


def test_strawberry():
    response = requests.get(settings.SITE_URL + 'graphql')
    assert response.status_code == 200