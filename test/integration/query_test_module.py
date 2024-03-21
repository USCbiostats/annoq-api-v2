from src.main import schema
import pytest

@pytest.mark.asyncio
async def test_query():
    query = """
        query myQuery {
            GetSNPsByIDs(ids: ["2:10662G>C", "2:10632C>A"], page_args: {from_: 0, size: 5}) {
                chr {
                    aggs {
                        doc_count
                        histogram{
                            key
                            doc_count
                        }
                    }
                    value
                },
                id,
                pos{
                    aggs{
                        min,
                            max
                    }
                    value
                }
            }
        }
    """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert len(result.data['GetSNPsByIDs']) == 2
    assert result.data['GetSNPsByIDs'][0]['chr']['value'] == '2'
    assert result.data['GetSNPsByIDs'][0]['chr']['aggs'] is None
    assert result.data['GetSNPsByIDs'][0]['pos']['value'] == '10662'

