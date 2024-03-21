from fastapi.testclient import TestClient
from src.main import app
import json

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_read_annotations():
    response = client.get("/annotations")
    assert response.status_code == 200
    with open('./data/api_mapping_anno_tree.json') as f:
        data = json.load(f)
        assert response.json() == data

