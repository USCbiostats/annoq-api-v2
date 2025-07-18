from src.data_adapter.snp_attributes import get_keyword_searchable_set

def keyword_query(keyword: str, keyword_fields:list[str] = None, filter_fields:list[str] = None):
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
      searchable_fields = list(get_keyword_searchable_set())
    else:
      searchable_fields = keyword_fields  
      
    query = {
      "bool": {
        "must": {
          "multi_match": {
            "query": keyword,
            "fields": searchable_fields
          }
        }
      }
    }
    
    if filter_fields and len(filter_fields) > 0:
      query["bool"]["filter"] = []
      for field in filter_fields:
        if field == 'id':
            field = '_id'
        query["bool"]["filter"].append({"exists": {"field": field}})
    
    # print(f'Keyword query {str(query)}')
    return query
  
  
  
  

    # query = {
    #           "multi_match": {
    #             "query": keyword,
    #             "fields": searchable_fields
    #           }
    #       }

    return query