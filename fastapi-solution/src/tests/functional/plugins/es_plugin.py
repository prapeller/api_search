from typing import Iterable

import pytest_asyncio
from elasticsearch import AsyncElasticsearch, NotFoundError

from tests.functional.settings import test_settings
from tests.functional.utils.helpers import get_es_bulk_query_str


@pytest_asyncio.fixture
async def es_client():
    es_client = AsyncElasticsearch(hosts=f'http://{test_settings.ELASTIC_HOST}:{test_settings.ELASTIC_PORT}',
                                   validate_cert=False,
                                   use_ssl=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture
def es_load_test_objs(es_client):
    async def inner(objs: list[dict], index: str):
        bulk_query_str = get_es_bulk_query_str(objs, index)
        response = await es_client.bulk(body=bulk_query_str, refresh=True)
        if response['errors']:
            raise Exception('error while loading to Elasticsearch')

    return inner


@pytest_asyncio.fixture
def es_delete_by_ids(es_client):
    async def inner(ids: Iterable[str]):
        try:
            await es_client.delete_by_query(index=test_settings.ELASTIC_INDEX_MOVIES,
                                            body={'query': {'ids': {'values': ids}}})
        except NotFoundError:
            pass
        try:
            await es_client.delete_by_query(index=test_settings.ELASTIC_INDEX_GENRES,
                                            body={'query': {'ids': {'values': ids}}})
        except NotFoundError:
            pass
        try:
            await es_client.delete_by_query(index=test_settings.ELASTIC_INDEX_PERSONS,
                                            body={'query': {'ids': {'values': ids}}})
        except NotFoundError:
            pass

    return inner
