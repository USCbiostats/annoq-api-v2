from graphql import GraphQLError
from src.main import schema
import pytest


@pytest.mark.asyncio_cooperative
async def test_CountAnnotations():
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
async def test_GetAnnotations():
    query = """
        query myQuery {
            annotations {
                chr
            }
        }
    """
 
    result = await schema.execute(
        query,
    )
 
    assert result.errors is None
    assert len(result.data['annotations']) == 20


@pytest.mark.asyncio_cooperative
async def test_GetSNPsByChromosome():
    query = """
        query myQuery {
            get_SNPs_by_chromosome(
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
    assert len(result.data['get_SNPs_by_chromosome']) == 0


@pytest.mark.asyncio_cooperative
async def test_GetSNPsByIDs():
    query = """
        query myQuery {
            get_SNPs_by_IDs(ids: ["2:10662G>C", "2:10632C>A"], page_args: {from_: 0, size: 5}) {
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
    assert len(result.data['get_SNPs_by_IDs']) == 2
    assert result.data['get_SNPs_by_IDs'][0]['chr'] == '2'
    assert result.data['get_SNPs_by_IDs'][0]['pos'] == 10662


@pytest.mark.asyncio_cooperative
async def test_CountSNPsByIDs():
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
            count_Snps_by_pos(pos: "10662")
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