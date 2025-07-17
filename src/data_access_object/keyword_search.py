from src.data_adapter.snp_attributes import get_keyword_searchable_fields

def keyword_query(keyword: str, keyword_fields:list[str] = None):
    """
    Query for getting annotation by keyword

    Params: keyword: Keyword for search

    Returns: Query for elasticsearch
    """

    searchable_fields = []
    # with open('./data/anno_tree.json') as f:
    #     data = json.load(f)
    #     searchable_fields = [elt['name'] for elt in data if data.get('keyword_searchable', False)]
    if keyword_fields is None:
      searchable_fields = get_keyword_searchable_fields()
    else:
      searchable_fields = keyword_fields  

    query = {
              "multi_match": {
                "query": keyword,
                "fields": searchable_fields
              }
          }

    return query