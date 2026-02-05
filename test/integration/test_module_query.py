from graphql import GraphQLError
from src.config.settings import settings
from src.main import schema
import pytest


@pytest.mark.asyncio_cooperative
async def test_count_annotations():
    query = """
        query myQuery {
            count_annotations
        }
    """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert result.data['count_annotations'] == 449


@pytest.mark.asyncio_cooperative
async def test_get_annotations():
    query = """
        query myQuery {
            annotations {
                snps{
                    chr
                }
            }
        }
    """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert len(result.data['annotations']['snps']) == 20


@pytest.mark.asyncio_cooperative
async def test_get_SNPs_by_chromosome():
    query = """
        query myQuery {
            get_SNPs_by_chromosome(
                chr: "2"
                end: 100000
                start: 10
                query_type_option: SNPS
                page_args: {from_: 10, size: 10}
            ) {
                snps{
                    chr
                    pos
                }
            }
        }
    """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert len(result.data['get_SNPs_by_chromosome']['snps']) == 0


@pytest.mark.asyncio_cooperative
async def test_get_SNPs_by_IDs():
    query = """
        query myQuery {
            get_SNPs_by_IDs(ids: ["2:10662G>C", "2:10632C>A"], query_type_option: SNPS, page_args: {from_: 0, size: 5}) {
                snps{
                    chr
                    pos
                    id
                }  
            }
        }
    """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert len(result.data['get_SNPs_by_IDs']['snps']) == 2
    assert result.data['get_SNPs_by_IDs']['snps'][0]['chr'] == '2'
    assert result.data['get_SNPs_by_IDs']['snps'][0]['pos'] == 10662


@pytest.mark.asyncio_cooperative
async def test_count_SNPs_by_IDs():
    query = """
        query myQuery {
            count_SNPs_by_IDs(ids: "2:10662G>C")
        }
    """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert result.data['count_SNPs_by_IDs'] == 1


@pytest.mark.asyncio_cooperative
async def test_wrong_query():
    query = """
        query myQuery {
            count_SNPs_by_pos(pos: "10662")
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
            get_SNPs_by_chromosome(
                chr: "2"
                end: 100000
                start: 10
                query_type_option: SNPS
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
async def test_get_aggs_by_RsIDs():
    query = """
        query MyQuery {
            get_aggs_by_RsIDs(rsIDs: ["rs189126619"], histogram: {interval: 10, max: 1000, min: 0}){
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
    assert result.data['get_aggs_by_RsIDs']['chr']['doc_count'] == 1
    #assert result.data['get_aggs_by_RsIDs']['rs_dbSNP151']['min'] == 10632
    #assert result.data['get_aggs_by_RsIDs']['rs_dbSNP151']['max'] == 10632
    assert result.data['get_aggs_by_RsIDs'][settings.DATA_RSID]['min'] == 10632
    assert result.data['get_aggs_by_RsIDs'][settings.DATA_RSID]['max'] == 10632

@pytest.mark.asyncio_cooperative
async def test_get_SNPs_by_chromosome():
    query = """
        query MyQuery {
            get_SNPs_by_chromosome(chr: "2", end: 1000000, start: 1, query_type_option: SNPS, filter_args: {exists: ["ALSPAC_AC"]}){
                snps{
                    chr
                }
            }
        }
        """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert len(result.data['get_SNPs_by_chromosome']['snps']) == 0


@pytest.mark.asyncio_cooperative
async def test_download_SNPs_by_chromosome():
    query = """
        query MyQuery {
            download_SNPs_by_chromosome(chr: "3", end: 1000000, fields: ["chr"], start: 10)
        }
        """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert result.data['download_SNPs_by_chromosome'].split('/')[1] == 'downloads'