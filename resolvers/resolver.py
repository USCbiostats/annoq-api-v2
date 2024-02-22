
from typing import List
from itertools import islice
from config.es import es
from config.settings import settings
from models.model import AnnoqData

async def search_by_ID(id:str):

    response = await es.get(
        index = settings.ES_INDEX,
        id = id
    )

    results = AnnoqData(id=response['_id'], **dict(islice(response['_source'].items(), 10)))

    return results


async def get_annotations():
    resp = await es.search(
          index=settings.ES_INDEX,
          query={"match_all": {}},
          size=20,
    )

    results = [AnnoqData(id=hit['_id'], 
                         chr = hit['_source']['chr'],
                         pos = hit['_source']['pos'],
                         ref = hit['_source']['ref'],
                         alt = hit['_source']['alt'],
                         ANNOVAR_ensembl_Effect = hit['_source']['ANNOVAR_ensembl_Effect'],
                         ANNOVAR_ensembl_Transcript_ID = hit['_source'].get('ANNOVAR_ensembl_Transcript_ID', None),
                         ANNOVAR_ensembl_Gene_ID = hit['_source'].get('ANNOVAR_ensembl_Gene_ID', None),
                         ANNOVAR_ensembl_summary = hit['_source']['ANNOVAR_ensembl_summary'],
                         SnpEff_ensembl_Effect = hit['_source']['SnpEff_ensembl_Effect'],
                         SnpEff_ensembl_Effect_impact = hit['_source']['SnpEff_ensembl_Effect_impact']) 
              for hit in resp['hits']['hits']]
        
    return results