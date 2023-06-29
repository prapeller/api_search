import uuid

from tests.functional.utils.helpers import get_ids_objs


def get_id_genre() -> tuple[str, dict]:
    id = str(uuid.uuid4())
    genre: dict = {
        'id': id,
        'name': 'Test Genre',
        'films': [
            {'id': str(uuid.uuid4()), 'title': 'Test Film1'},
            {'id': str(uuid.uuid4()), 'title': 'Test Film2'},
        ],
    }
    return id, genre


def get_ids_genres(qty: int) -> tuple[list[str], list[dict]]:
    return get_ids_objs(qty, get_id_genre)
