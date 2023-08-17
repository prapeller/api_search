from http import HTTPStatus

import orjson
import pytest

from core.enums import ResponseDetailEnum, GenreFilterByEnum, FilterConditionsEnum
from db.models.genre import Genre
from tests.functional.settings import test_settings
from tests.functional.testdata.genres import get_ids_genres

pytestmark = pytest.mark.asyncio


async def test_get_api_v1_genres_list(es_load_test_objs, es_delete_by_ids, body_status):
    """Test that if no params passed - route will return:
     - status 200
     - response body will have 'total_count' key with total number of genres
     - response body will have 'genres' key with genres list and it will have length == 20
     """
    ids, genres_25 = get_ids_genres(qty=25)
    await es_load_test_objs(genres_25, test_settings.ELASTIC_INDEX_GENRES)
    url = f'http://{test_settings.API_SEARCH_HOST}:{test_settings.API_SEARCH_PORT}/api/v1/genres'

    body, status = await body_status(url)

    assert status == HTTPStatus.OK
    assert isinstance(body.get('total_count'), int)
    assert len(body.get('objs')) == 20

    await es_delete_by_ids(ids)


async def test_get_api_v1_genres_search_existing(es_load_test_objs, es_delete_by_ids, body_status):
    """Test that if search params of existing films passed - route will return:
     - status 200
     - response body will have 'total_count' key with total number of genres
     - response body will have 'genres' key with genres list and it will have length == 20
     """
    ids, genres_25 = get_ids_genres(qty=25)
    await es_load_test_objs(genres_25, test_settings.ELASTIC_INDEX_GENRES)
    url = f'http://{test_settings.API_SEARCH_HOST}:{test_settings.API_SEARCH_PORT}/api/v1/genres/search'
    query_params = {'field': GenreFilterByEnum.name, 'condition': FilterConditionsEnum.includes, 'value': 'Test Genre'}

    body, status = await body_status(url, query_params)

    assert status == HTTPStatus.OK
    assert isinstance(body.get('total_count'), int)
    assert len(body.get('objs')) == 20

    await es_delete_by_ids(ids)


async def test_get_api_v1_genres_search_not_existing(body_status):
    """Test that if search params of not existing films passed - route will return:
     - status 404
     - response body with explanation value string by 'detail' key string
     """
    url = f'http://{test_settings.API_SEARCH_HOST}:{test_settings.API_SEARCH_PORT}/api/v1/genres/search'
    query_params = {'field': GenreFilterByEnum.name, 'condition': FilterConditionsEnum.includes, 'value': 'abracadabra'}

    body, status = await body_status(url, query_params)

    assert status == HTTPStatus.NOT_FOUND
    assert body.get('detail') == ResponseDetailEnum.genres_not_found


async def test_get_api_v1_genres_search_not_valid_params(es_load_test_objs, es_delete_by_ids, body_status):
    """Test that if search params are not valid - route will return:
     - status 422
     - response body will have msg about it
     """
    ids, genres_25 = get_ids_genres(qty=25)
    await es_load_test_objs(genres_25, test_settings.ELASTIC_INDEX_GENRES)
    url = f'http://{test_settings.API_SEARCH_HOST}:{test_settings.API_SEARCH_PORT}/api/v1/genres/search'
    query_params = {'field': 'not_existing_field', 'condition': 'not_existing_cond', 'value': 'Test Genre'}

    body, status = await body_status(url, query_params)

    assert status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert 'value is not a valid enumeration member' in body.get('detail')[0]['msg']

    await es_delete_by_ids(ids)


async def test_get_api_v1_genres_by_id(es_load_test_objs, es_delete_by_ids, body_status):
    """Test that if id of existing film passed to path param - route will return:
     - status 200
     - response body will have Genre model fields
     """
    ids, genres_1 = get_ids_genres(qty=1)
    await es_load_test_objs(genres_1, test_settings.ELASTIC_INDEX_GENRES)
    url = f'http://{test_settings.API_SEARCH_HOST}:{test_settings.API_SEARCH_PORT}/api/v1/genres/{ids[0]}'

    body, status = await body_status(url)

    assert status == HTTPStatus.OK
    assert Genre(**body).json() == orjson.dumps(body).decode()

    await es_delete_by_ids(ids)


async def test_get_api_v1_genres_by_not_valid_id(es_load_test_objs, es_delete_by_ids, body_status):
    """Test that if {id} parameter passed not UUID - route will return:
     - status 422
     - response body will have msg about it
     """
    ids, genres_1 = get_ids_genres(qty=1)
    await es_load_test_objs(genres_1, test_settings.ELASTIC_INDEX_GENRES)
    url = f'http://{test_settings.API_SEARCH_HOST}:{test_settings.API_SEARCH_PORT}/api/v1/genres/not-a-uuid'

    body, status = await body_status(url)

    assert status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert body.get('detail')[0]['msg'] == 'value is not a valid uuid'

    await es_delete_by_ids(ids)
