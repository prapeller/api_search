import json


def get_ids_objs(qty: int, func) -> tuple[list[str], list[dict]]:
    ids = []
    objs = []
    for _ in range(qty):
        id, obj_data = func()
        ids.append(id)
        objs.append(obj_data)
    return ids, objs


def get_es_bulk_query_str(objs: list[dict], index: str) -> str:
    bulk_query = []
    for obj in objs:
        bulk_query.extend([
            json.dumps({'index': {'_index': index, '_id': obj['id']}}),
            json.dumps(obj)
        ])

    return '\n'.join(bulk_query) + '\n'
