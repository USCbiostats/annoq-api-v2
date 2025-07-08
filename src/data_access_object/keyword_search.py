from src.data_adapter.snp_attributes import get_keyword_searchable_fields

def keyword_query(keyword: str):
    """
    Query for getting annotation by keyword

    Params: keyword: Keyword for search

    Returns: Query for elasticsearch
    """

    searchable_fields = []
    # with open('./data/anno_tree.json') as f:
    #     data = json.load(f)
    #     searchable_fields = [elt['name'] for elt in data if data.get('keyword_searchable', False)]
    searchable_fields = get_keyword_searchable_fields()

    query = {
              "multi_match": {
                "query": keyword,
                "fields": searchable_fields
              }
          }

    return query