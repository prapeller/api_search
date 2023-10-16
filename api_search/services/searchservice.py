import json
import logging
from abc import ABC, abstractmethod

import backoff
import pydantic as pd
from elasticsearch import (AsyncElasticsearch, NotFoundError,
                           ConnectionError, ConnectionTimeout, TransportError)
from elasticsearch_dsl import Q

from core import config
from core.enums import ElasticIndexEnum, FilterConditionsEnum
from db.models.film import Film
from db.models.genre import Genre
from db.models.person import Person
from helpers.backoff_handler import elastic_backoff
from services.cache import Cache

logger = logging.getLogger(__name__)


class SearchService(ABC):

    @abstractmethod
    async def get_by_id(self, *args, **kwargs):
        pass

    @abstractmethod
    async def count(self, *args, **kwargs):
        pass

    @abstractmethod
    async def search(self, *args, **kwargs):
        pass

    @abstractmethod
    async def order(self, *args, **kwargs):
        pass

    @abstractmethod
    async def limit_offset(self, *args, **kwargs):
        pass

    @abstractmethod
    async def filter(self, *args, **kwargs):
        pass


class ElasticSearchService(SearchService):
    def __init__(self,
                 cache: Cache,
                 elastic: AsyncElasticsearch,
                 index: ElasticIndexEnum,
                 Model: type[pd.BaseModel]):
        self.cache = cache
        self.elastic = elastic
        self.index = index
        self.Model = Model
        self.query = {}

    async def get_by_id(self, id: str) -> pd.BaseModel | None:
        cache = await self.cache.get_cache(id)
        if cache is None:
            obj = await self._get_by_id_from_elastic(id)
            if not obj:
                return None
            await self._set_obj_to_cache(obj)
            return obj
        if cache:
            return self.Model.parse_raw(cache)

    @backoff.on_exception(backoff.expo,
                          (ConnectionError, TransportError,
                           ConnectionTimeout, ConnectionRefusedError),
                          max_time=config.ELASTIC_BACKOFF_MAX_TIME_SEC,
                          jitter=None,
                          on_backoff=elastic_backoff)
    async def count(self) -> int:
        response = await self.elastic.count(index=self.index, body={'query': {'match_all': {}}})
        return response['count']

    @backoff.on_exception(backoff.expo,
                          (ConnectionError, TransportError,
                           ConnectionTimeout, ConnectionRefusedError),
                          max_time=config.ELASTIC_BACKOFF_MAX_TIME_SEC,
                          jitter=None,
                          on_backoff=elastic_backoff)
    async def _get_objs_from_elastic(self, query) -> list[Film | Genre | Person]:
        logger.info('execute search query from elastic')
        results = await self.elastic.search(index=self.index, body=query)
        objs = []
        for hit in results['hits']['hits']:
            objs.append(hit['_source'])
        return objs

    @backoff.on_exception(backoff.expo,
                          (ConnectionError, TransportError,
                           ConnectionTimeout, ConnectionRefusedError),
                          max_time=config.ELASTIC_BACKOFF_MAX_TIME_SEC,
                          jitter=None,
                          on_backoff=elastic_backoff)
    async def _get_by_id_from_elastic(self, id: str) -> pd.BaseModel | None:
        try:
            doc = await self.elastic.get(index=self.index, id=id)
        except NotFoundError:
            return None
        return self.Model(**doc['_source'])

    async def _set_obj_to_cache(self, obj: pd.BaseModel):
        id = str(obj.id)
        data = obj.json()
        await self.cache.set_cache(id, data)

    async def search(self) -> list[pd.BaseModel]:
        logger.info(f'search {self.query=:}')
        query_is_cachable = 'from' not in self.query.keys() and self.query.get('size') in [20, 100, 500]

        if query_is_cachable:
            cache_key = f'{self.index} {json.dumps(self.query, sort_keys=True)}'
            cache = await self.cache.get_cache(cache_key)
            if cache:
                objs = json.loads(cache)
            else:
                objs = await self._get_objs_from_elastic(self.query)
                objs_data = json.dumps(objs)
                await self.cache.set_cache(cache_key, objs_data)
            return objs

        else:
            return await self._get_objs_from_elastic(self.query)

    async def order(self, order_by: str, order: str) -> None:
        fields_nested = tuple(order_by.split('.'))

        # ordering by nested
        if len(fields_nested) > 1 and fields_nested[1] != 'raw':
            self.query['sort'] = [{order_by: {"order": order, "nested": {"path": fields_nested[0]}}}]

        # ordering by flat
        else:
            self.query['sort'] = [{order_by: {"order": order}}]

    async def limit_offset(self, limit: int | None, offset: int) -> None:
        if offset:
            self.query['from'] = offset
        if limit:
            self.query['size'] = limit

    async def filter(self, **filter_params) -> None:
        if filter_params:
            assert filter_params.get('field') is not None
            assert filter_params.get('condition') is not None
            assert filter_params.get('value') is not None

            field = filter_params.get('field')
            fields_nested = tuple(field.split('.'))
            condition = filter_params.get('condition')
            assert condition in FilterConditionsEnum, \
                f'possible conditions for filtering: {tuple(cond for cond in FilterConditionsEnum)}'
            value = filter_params.get('value')
            flat_field = fields_nested[0]

            # filtering by nested 'one.two.raw'
            if len(fields_nested) > 1 and fields_nested[1] != 'raw':

                path = flat_field
                nested_fields_str = '__'.join(field for field in fields_nested)

                if condition == FilterConditionsEnum.includes:
                    nested_query = Q('nested', path=path, query=Q('match', **{nested_fields_str: value}))
                    self.query['query'] = nested_query.to_dict()

                elif condition in (FilterConditionsEnum.lt,
                                   FilterConditionsEnum.lte,
                                   FilterConditionsEnum.gt,
                                   FilterConditionsEnum.gte):
                    pass

            # filtering by flat 'one.raw' by flat 'one'
            elif (len(fields_nested) > 1 and fields_nested[1] == 'raw') or len(fields_nested) == 1:
                field = flat_field

                if condition == FilterConditionsEnum.includes:
                    self.query['query'] = Q('match', **{field: value}).to_dict()

                elif condition in (FilterConditionsEnum.lt,
                                   FilterConditionsEnum.lte,
                                   FilterConditionsEnum.gt,
                                   FilterConditionsEnum.gte):
                    self.query['query'] = Q('range', **{field: {condition: value}}).to_dict()
