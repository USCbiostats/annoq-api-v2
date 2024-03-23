import uuid
from ...config.es import es
from ...config.settings import settings


async def download_annotations(fields: list[str], resp: dict):
    count = 0
    filename = str(uuid.uuid4()) + '.txt'
    f = open(settings.DOWNLOAD_DIR + '/' + filename, 'w')
    f.write('\t'.join(fields) + '\n')

    old_scroll_id = resp['_scroll_id']

    while len(resp['hits']['hits']):
        for doc in resp['hits']['hits']:
            count += 1
            if count > settings.DOWNLOAD_SIZE: 
                return "/download/" + 'tmp/' + filename
            
            li = [str(doc['_source'].get(k, '.')) for k in fields]
            f.write('\t'.join(li) + "\n")

        resp = await es.scroll(
            scroll_id = old_scroll_id,
            scroll = '2s'
        )

        if old_scroll_id != resp['_scroll_id']:
            f.write("download error on:", resp['_scroll_id'])

        old_scroll_id = resp['_scroll_id']

    return "/download/" + 'tmp/' + filename
