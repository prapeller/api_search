import logging
from time import sleep

from config import settings
from helpers.extract import PostgresExtractor
from helpers.load import ElasticSearchSender
from helpers.stateman import StateManager
from helpers.transform import transform

logging.basicConfig(level=logging.INFO)
logging.getLogger('backoff').addHandler(logging.StreamHandler())

if __name__ == '__main__':
    state_manager = StateManager(settings.STATE_FILENAME)

    es_sender = ElasticSearchSender(settings.ELASTIC_HOST, settings.ELASTIC_PORT)
    pse = PostgresExtractor({
        'host': settings.POSTGRES_HOST,
        'port': settings.POSTGRES_PORT,
        'database': settings.POSTGRES_DB,
        'user': settings.POSTGRES_USER,
        'password': settings.POSTGRES_PASSWORD,
    }, state_manager)
    es_sender.create_index(settings.ELASTIC_MOVIES)
    es_sender.create_index(settings.ELASTIC_GENRES)
    es_sender.create_index(settings.ELASTIC_PERSONS)
    while True:
        movie_data = pse.get_films_data()
        tformed_data = transform(movie_data)
        es_sender.send_data(tformed_data)
        state_manager.save_state()
        sleep(settings.TIMEOUT)
