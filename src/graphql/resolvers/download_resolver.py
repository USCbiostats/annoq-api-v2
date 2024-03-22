import uuid
from ...config.es import es
from ...config.settings import settings
from .helper_resolver import annotation_query, convert_hits, get_aggregation_query


async def download_annotations(es_fields: list[str]):
    count = 0
    filename = str(uuid.uuid4()) + '.txt'
    f = open(settings.DOWNLOAD_DIR + '/' + filename, 'w')
    f.write('\t'.join(es_fields) + '\n')
    resp = await es.search(
        index = settings.ES_INDEX,
        scroll = '2m',
        source = es_fields,
        query = annotation_query(),
        aggs = await get_aggregation_query(es_fields),
        size = 20
    )
    old_scroll_id = resp['_scroll_id']

    while len(resp['hits']['hits']):
        for doc in resp['hits']['hits']:
            count += 1
            if count > settings.DOWNLOAD_SIZE: 
                results = convert_hits(resp['hits']['hits'], None)  
                return results
            
            li = [str(doc['_source'].get(k, '.')) for k in es_fields]
            f.write('\t'.join(li) + "\n")

        resp = await es.scroll(
            scroll_id = old_scroll_id,
            scroll = '2s' # length of time to keep search context
        )
        # check if there's a new scroll ID
        if old_scroll_id != resp['_scroll_id']:
            f.write("download error on:", resp['_scroll_id'])

        old_scroll_id = resp['_scroll_id']

    results = convert_hits(resp['hits']['hits'], None)  
    return results
