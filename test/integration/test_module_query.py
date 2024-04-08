from graphql import GraphQLError
from src.main import schema
import pytest


@pytest.mark.asyncio_cooperative
async def test_CountAnnotations():
    query = """
        query myQuery {
            CountAnnotations
        }
    """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert result.data['CountAnnotations'] == 99


@pytest.mark.asyncio_cooperative
async def test_GetAnnotations():
    query = """
        query myQuery {
            GetAnnotations {
                chr
            }
        }
    """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert len(result.data['GetAnnotations']) == 20


@pytest.mark.asyncio_cooperative
async def test_GetSNPsByChromosome():
    query = """
        query myQuery {
            GetSNPsByChromosome(
                chr: "2"
                end: 100000
                start: 10
                page_args: {from_: 10, size: 10}
            ) {
                chr
            		pos
            }
        }
    """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert len(result.data['GetSNPsByChromosome']) == 0


@pytest.mark.asyncio_cooperative
async def test_GetSNPsByIDs():
    query = """
        query myQuery {
            GetSNPsByIDs(ids: ["2:10662G>C", "2:10632C>A"], page_args: {from_: 0, size: 5}) {
                chr
                pos
                id
            }
        }
    """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert len(result.data['GetSNPsByIDs']) == 2
    assert result.data['GetSNPsByIDs'][0]['chr'] == '2'
    assert result.data['GetSNPsByIDs'][0]['pos'] == 10662


@pytest.mark.asyncio_cooperative
async def test_CountSNPsByIDs():
    query = """
        query myQuery {
            CountSNPsByIDs(ids: "2:10662G>C")
        }
    """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert result.data['CountSNPsByIDs'] == 1


@pytest.mark.asyncio_cooperative
async def test_wrong_query():
    query = """
        query myQuery {
            CountSnpsByPos(pos: "10662")
        }
    """
 
    result = await schema.execute(
        query,
    )
 
    assert any(isinstance(error, GraphQLError) for error in result.errors)


@pytest.mark.asyncio_cooperative
async def test_wrong_key():
    query = """
        query myQuery {
            GetSNPsByChromosome(
                chr: "2"
                end: 100000
                start: 10
                page_args: {from_: 10, size: 10}
            ) {
                last_name {
                    value
                }
            }
        }
    """
 
    result = await schema.execute(
        query,
    )
 
    assert any(isinstance(error, GraphQLError) for error in result.errors)


@pytest.mark.asyncio_cooperative
async def test_GetAggsByRsIDs():
    query = """
        query MyQuery {
            GetAggsByRsIDs(rsIDs: ["rs189126619"], histogram: {interval: 10, max: 1000, min: 0}){
                chr{
                doc_count
                histogram{
                    doc_count
                    key
                }
                }
                rs_dbSNP151{
                min
                max
                }
            }
            }
        """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert result.data['GetAggsByRsIDs']['chr']['doc_count'] == 1
    assert result.data['GetAggsByRsIDs']['rs_dbSNP151']['min'] == 10632
    assert result.data['GetAggsByRsIDs']['rs_dbSNP151']['max'] == 10632


@pytest.mark.asyncio_cooperative
async def test_GetAggsByRsIDs():
    query = """
        query MyQuery {
            GetSNPsByChromosome(chr: "2", end: 1000000, start: 1, filter_args: {exists: ["ALSPAC_AC"]}){
                chr
            }
        }
        """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert len(result.data['GetSNPsByChromosome']) == 0


@pytest.mark.asyncio_cooperative
async def test_DownloadSNPsByChromosome():
    query = """
        query MyQuery {
            DownloadSNPsByChromosome(chr: "3", end: 1000000, fields: ["chr"], start: 10)
        }
        """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert result.data['DownloadSNPsByChromosome'].split('/')[1] == 'downloads'