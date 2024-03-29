import json
import typing as tp
from functools import lru_cache

import fastapi as fa
import httpx
import pydantic as pd
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis

from core.config import settings
from core.enums import (
    FilterConditionsEnum,
    FilmFilterByEnum,
    GenreFilterByEnum,
    PersonFilterByEnum,
    ElasticIndexEnum,
    ServicesNamesEnum,
)
from core.exceptions import UnauthorizedException
from core.logger_config import logger
from db.models.film import Film
from db.models.genre import Genre
from db.models.person import PersonFilms
from services.cache import RedisCache
from services.searchservice import ElasticSearchService

es: AsyncElasticsearch | None = None


async def elastic_dependency() -> AsyncElasticsearch:
    return es


redis: Redis | None = None


async def redis_dependency() -> Redis:
    return redis


async def pagination_params_dependency(
        # pagination params with defaults: offset = 0 / limit = 20
        offset: tp.Annotated[int, fa.Query(description='objects selection display offset', ge=0)] = 0,
        limit: tp.Annotated[int, fa.Query(description='limiting number of objects selection', gt=0)] = 20,
):
    return {
        'offset': offset,
        'limit': limit,
    }


async def film_filter_params_dependency(
        field: tp.Annotated[FilmFilterByEnum, fa.Query(description='field of film to filter by')] = None,
        condition: tp.Annotated[FilterConditionsEnum, fa.Query(description='condition of filtering')] = None,
        value: tp.Annotated[str, fa.Query(description='value to filter by')] = None
):
    return {'field': field,
            'condition': condition,
            'value': value}


async def genre_filter_params_dependency(
        field: tp.Annotated[GenreFilterByEnum, fa.Query(description='field of genre to filter by')] = None,
        condition: tp.Annotated[FilterConditionsEnum, fa.Query(description='condition of filtering')] = None,
        value: tp.Annotated[str, fa.Query(description='value to filter by')] = None
):
    return {'field': field,
            'condition': condition,
            'value': value}


async def person_filter_params_dependency(
        field: tp.Annotated[PersonFilterByEnum, fa.Query(description='field of person to filter by')] = None,
        condition: tp.Annotated[FilterConditionsEnum, fa.Query(description='condition of filtering')] = None,
        value: tp.Annotated[str, fa.Query(description='value to filter by')] = None
):
    return {'field': field,
            'condition': condition,
            'value': value}


async def cache_dependency(
        redis: Redis = Depends(redis_dependency),
) -> RedisCache:
    return RedisCache(redis)


@lru_cache()
def es_service_dependency(
        index: ElasticIndexEnum,
        Model: type[pd.BaseModel],
        cache: RedisCache = Depends(cache_dependency),
        elastic: AsyncElasticsearch = Depends(elastic_dependency),
) -> ElasticSearchService:
    return ElasticSearchService(cache, elastic, index, Model)


def es_service_film_dependency(
        cache: RedisCache = Depends(cache_dependency),
        elastic: AsyncElasticsearch = Depends(elastic_dependency),
):
    return es_service_dependency(ElasticIndexEnum.movies, Film, cache, elastic)


def es_service_genre_dependency(
        cache: RedisCache = Depends(cache_dependency),
        elastic: AsyncElasticsearch = Depends(elastic_dependency),
):
    return es_service_dependency(ElasticIndexEnum.genres, Genre, cache, elastic)


def es_service_person_dependency(
        cache: RedisCache = Depends(cache_dependency),
        elastic: AsyncElasticsearch = Depends(elastic_dependency),
):
    return es_service_dependency(ElasticIndexEnum.persons, PersonFilms, cache, elastic)


oauth2_scheme_local = OAuth2PasswordBearer(
    tokenUrl=f"http://{settings.API_AUTH_HOST}:{settings.API_AUTH_PORT}/api/v1/auth/login")


async def verified_access_token_dependency(
        request: fa.Request,
        access_token: str = fa.Depends(oauth2_scheme_local),
) -> dict:
    url = f"http://{settings.API_AUTH_HOST}:{settings.API_AUTH_PORT}/api/v1/auth/verify-access-token"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = {
        'useragent': request.headers.get("user-agent"),
        'ip': request.headers.get('X-Forwarded-For'),
        'access_token': access_token,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json=data)
    if resp.status_code != fa.status.HTTP_200_OK:
        raise UnauthorizedException
    return json.loads(resp.text)


async def verify_service_dependency(
        request: fa.Request,
) -> None:
    auth_header = request.headers.get('Authorization')
    service_name = request.headers.get('Service-Name')
    if (not auth_header
            or service_name not in [str(s) for s in ServicesNamesEnum]
            or auth_header != settings.SERVICE_TO_SERVICE_SECRET):
        detail = f"can't verify service request: {auth_header=:} {service_name=:}"
        logger.error(detail)
        raise UnauthorizedException(detail)
