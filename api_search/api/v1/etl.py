from pathlib import Path

import fastapi as fa

from services.etl.etl import extract_and_load

router = fa.APIRouter()

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


@router.post("/extract-from-postgres-load-to-elastic-all", status_code=fa.status.HTTP_201_CREATED)
def etl_extract_from_postgres_load_to_elastic():
    extract_and_load(table_name='film_work',
                     json_storage_path=ROOT_DIR / 'services/etl/json_storage.json',
                     index_name='movies',
                     index_schema_path=ROOT_DIR / 'db/schemas/elastic_index_movies.json',
                     chunk_size=500,
                     )
    return {'message': 'ok'}


@router.post("/extract-from-postgres-load-to-elastic-by-id-list", status_code=fa.status.HTTP_201_CREATED)
def etl_extract_from_postgres_load_to_elastic_by_id_list(
        id_list: list[str]
):
    extract_and_load(table_name='film_work',
                     json_storage_path=ROOT_DIR / 'services/etl/json_storage.json',
                     index_name='movies',
                     index_schema_path=ROOT_DIR / 'db/schemas/elastic_index_movies.json',
                     chunk_size=500,
                     id_list=id_list
                     )
    return {'message': 'ok'}
