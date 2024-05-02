import uuid
from ...config.es import es
from ...config.settings import settings


async def download_annotations(fields: list[str], resp: dict):
    """
    Download annotations from elasticsearch

    Params: fields: List of fields to be returned in elasticsearch query
            resp: elasticsearch response object

    Returns: string for download filename
    """
    count = 0
    filename = str(uuid.uuid4()) + '.txt'
    f = open(settings.DOWNLOAD_DIR + '/' + filename, 'w')
    f.write('\t'.join(fields) + '\n')

    old_scroll_id = resp['_scroll_id']

    while len(resp['hits']['hits']):
        for doc in resp['hits']['hits']:
            count += 1
            if count > settings.DOWNLOAD_SIZE: 
                return "/downloads/" + filename
            
            li = []
            for k in fields:
                if k == "id":
                    li.append(str(doc['_id']))
                else:
                    li.append(str(doc['_source'].get(k, '.')))
            f.write('\t'.join(li) + "\n")

        resp = await es.scroll(
            scroll_id = old_scroll_id,
            scroll = '2s'
        )

        if old_scroll_id != resp['_scroll_id']:
            f.write("download error on:", resp['_scroll_id'])

        old_scroll_id = resp['_scroll_id']

    return "/downloads/" + filename
