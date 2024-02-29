from itertools import islice
from config.es import es
from config.settings import settings
from models.model import AnnoqSampleData, AnnoqDataType
import re

def to_graphql_name(name):
    if name[0].isdigit():
        return f"x_{name}"
    name = re.sub(r'\([^)]*\)', '', name)
    name = re.sub(r'\/[^\/]*', '', name)
    name = name.replace('-', '_')
    name = name.replace('+', '')
    return name

# Sample
def convert_hits(hits):
    compliant_results = []
    for hit in hits:
        source = hit['_source']
        compliant_source = {to_graphql_name(key): value for key, value in source.items()}
        compliant_results.append(AnnoqDataType(**compliant_source))
    return compliant_results


async def search_by_ID(id:str):

    response = await es.get(
        index = settings.ES_INDEX,
        id = id
    )

    results = [AnnoqSampleData(id=response['_id'], **dict(islice(response['_source'].items(), 10)))]

    return results


async def get_sample_annotations():
    resp = await es.search(
          index=settings.ES_INDEX,
          query={"match_all": {}},
          size=20
    )

    results = [AnnoqSampleData(id=hit['_id'], 
                         chr = hit['_source']['chr'],
                         pos = hit['_source']['pos'],
                         ref = hit['_source']['ref'],
                         alt = hit['_source']['alt'],
                         ANNOVAR_ensembl_Effect = hit['_source'].get('ANNOVAR_ensembl_Effect', None),
                         ANNOVAR_ensembl_Transcript_ID = hit['_source'].get('ANNOVAR_ensembl_Transcript_ID', None),
                         ANNOVAR_ensembl_Gene_ID = hit['_source'].get('ANNOVAR_ensembl_Gene_ID', None),
                         ANNOVAR_ensembl_summary = hit['_source']['ANNOVAR_ensembl_summary'],
                         SnpEff_ensembl_Effect = hit['_source']['SnpEff_ensembl_Effect'],
                         SnpEff_ensembl_Effect_impact = hit['_source']['SnpEff_ensembl_Effect_impact']) 
              for hit in resp['hits']['hits']]

        
    return results


async def get_annotations(es_fields: list[str]):
    resp = await es.search(
          index=settings.ES_INDEX,
          source=es_fields,
          query={"match_all": {}},
          size=20
    )

    results = convert_hits(resp['hits']['hits'])
        
    return results