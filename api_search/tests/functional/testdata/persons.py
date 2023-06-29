import uuid

from tests.functional.utils.helpers import get_ids_objs


def get_id_person() -> tuple[str, dict]:
    id = str(uuid.uuid4())
    person: dict = {
        'id': id,
        'name': 'Test Person',
        'films': [
            {'id': str(uuid.uuid4()), 'title': 'Test Film1'},
            {'id': str(uuid.uuid4()), 'title': 'Test Film2'},
        ],
    }
    return id, person


def get_ids_persons(qty: int) -> tuple[list[str], list[dict]]:
    return get_ids_objs(qty, get_id_person)
