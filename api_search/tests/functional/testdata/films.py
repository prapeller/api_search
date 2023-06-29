import random
import uuid

from tests.functional.utils.helpers import get_ids_objs


def get_id_film() -> tuple[str, dict]:
    id = str(uuid.uuid4())
    film: dict = {
        'id': id,
        'imdb_rating': random.randint(1, 10),
        'genre': [
            {'id': str(uuid.uuid4()), 'name': 'Action'},
            {'id': str(uuid.uuid4()), 'name': 'Comedy'},
        ],
        'title': 'Test Title',
        'description': 'Test Description',
        'director': [{'id': str(uuid.uuid4()), 'name': 'Test Director'}],
        'actors_names': ['Test Actor1', 'Test Actor2'],
        'writers_names': ['Test Writer1', 'Test Writer2'],
        'actors': [
            {'id': str(uuid.uuid4()), 'name': 'Test Actor1'},
            {'id': str(uuid.uuid4()), 'name': 'Test Actor2'},
        ],
        'writers': [
            {'id': str(uuid.uuid4()), 'name': 'Test Writer1'},
            {'id': str(uuid.uuid4()), 'name': 'Test Writer2'},
        ]
    }
    return id, film


def get_ids_films(qty: int) -> tuple[list[str], list[dict]]:
    return get_ids_objs(qty, get_id_film)
