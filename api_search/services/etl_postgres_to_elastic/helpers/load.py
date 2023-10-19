import json
import logging
from typing import Any, Dict, Generator, List

from backoff import expo, on_exception
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import (ConnectionError, ConnectionTimeout,
                                      TransportError)
from elasticsearch.helpers import BulkIndexError, streaming_bulk

from services.etl_postgres_to_elastic.config import BASE_DIR


class ElasticSearchSender:
    """
    Class for sending data to ES. Context managed.
    """

    def __init__(self, host: str, port: int, scheme: str = 'http'):
        self.index_name = None
        self.host = host
        self.port = port
        self.scheme = scheme
        self.client = None
        self.index_body = None

    def get_index_from_file(self, entity: str):
        with open(BASE_DIR / f'api_search/services/etl_postgres_to_elastic/{entity}_index.json') as file:
            logging.log(logging.INFO, f"Trying to open {entity + '_index.json'}")
            self.index_body = json.load(file)
            return self.index_body

    def __enter__(self):
        self.connect()
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def connect(self):
        self.client = Elasticsearch([{'host': self.host,
                                      'port': self.port,
                                      'scheme': self.scheme}])

    def _generate_movie_actions(self, data: List[Dict]) -> Generator[Dict, Any, Any]:
        """
        :param data:
        :return: Dict that match index schema
        """
        for row in data:
            doc = {
                '_id': row['uuid'],
                'uuid': row['uuid'],
                'imdb_rating': row['imdb_rating'],
                'genre': [{'uuid': g['uuid'],
                           'name': g['name']}
                          for g in row['genre'].values()],
                'title': row['title'],
                'description': row['description'],
                'director': [{'uuid': d['uuid'],
                              'name': d['full_name']}
                             for d in row['director'].values()] if row.get('director') else [],
                'actors_names': [a['full_name'] for a in row['actor'].values()] if row.get('actor') else [],
                'actors': [{'uuid': a['uuid'], 'name': a['full_name']} for a in row['actor'].values()] if row.get(
                    'actor') else [],
                'writers_names': [w['full_name'] for w in row['writer'].values()] if row.get('writer') else [],
                'writers': [{'uuid': w['uuid'], 'name': w['full_name']} for w in row['writer'].values()] if row.get(
                    'writer') else []
            }
            logging.log(logging.DEBUG, doc)
            yield doc

    def _generate_role_actions(self, data: List[Dict]) -> Generator[Dict, Any, Any]:
        for row in data:
            if row['uuid'] and row['name']:
                doc = {
                    '_id': row['uuid'],
                    'uuid': row['uuid'],
                    'name': row['name'],
                    'films': [{"uuid": f["uuid"], "title": f["title"], "imdb_rating": f["imdb_rating"]} for f in
                              row["films"].values()] if row.get("films") else []
                }
                logging.log(logging.DEBUG, doc)
                yield doc

    def _generate_genre_actions(self, data: List[Dict]) -> Generator[Dict, Any, Any]:
        for row in data:
            if row['uuid'] and row['name']:
                doc = {
                    '_id': row['uuid'],
                    'uuid': row['uuid'],
                    'name': row['name'],
                    'films': [{"uuid": f["uuid"], "title": f["title"]} for f in row["films"].values()] if row.get(
                        "films") else []
                }
                logging.log(logging.DEBUG, doc)
                yield doc

    @on_exception(expo, (ConnectionError, ConnectionTimeout, TransportError), max_tries=500)
    def send_data(self, data_dict: Dict[str, List[Dict]]):
        """
        Send bulk data to ElasticSearch. Context Managed, no need to wrap it 'with'
        :param data_dict:
        :return:
        """
        for entity, data in data_dict.items():
            with self as client:
                actions = {
                    "movies": self._generate_movie_actions,
                    "persons": self._generate_role_actions,
                    "genres": self._generate_genre_actions
                }[entity](data)

                try:
                    for action in streaming_bulk(client=client,
                                                 index=entity,
                                                 actions=actions
                                                 ):
                        logging.log(logging.DEBUG, action)
                except BulkIndexError as e:
                    logging.error(f"BulkIndexError: {e}")
                    logging.error(f"Failed documents: {e.errors}")

    @on_exception(expo, (ConnectionError, ConnectionTimeout, TransportError), max_tries=500)
    def create_index(self, index_name: str) -> None:
        """
        Trying to create index, ignores error 400 for case if it's already created
        Context Managed, no need to wrap it 'with'
        :return:
        """
        with self as client:
            client.indices.create(
                index=index_name,
                body=self.get_index_from_file(index_name),
                ignore=400,
            )
