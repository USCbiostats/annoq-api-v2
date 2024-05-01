import asyncio
import os
import json
from src.config.es import es
from src.config.settings import settings


async def process():
    files = os.listdir('./sample_data/downloaded_json_files')
    for filename in files:
        if filename.endswith('.json'):
            
            file = open('./sample_data/downloaded_json_files/' + filename, 'r')
            data = json.load(file)
            hits = data['hits']['hits']

            for elt in hits:
                await es.index(index=settings.ES_INDEX, body=elt['_source'], id=elt['_id'])

asyncio.run(process())
