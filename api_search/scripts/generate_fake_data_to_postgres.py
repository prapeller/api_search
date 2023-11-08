import json
import random
import time
import uuid
from datetime import datetime

import psycopg2
import requests
from psycopg2.extensions import cursor as ps_cursor

from core.config import settings

postgres_config = {
    'host': settings.POSTGRES_HOST,
    'port': settings.POSTGRES_PORT,
    'dbname': settings.POSTGRES_DB,
    'user': settings.POSTGRES_USER,
    'password': settings.POSTGRES_PASSWORD,
}


def get_random_uuids(table, quantity):
    cursor.execute(f"""
    select uuid from {table};
    """)
    all_uuids = [record[0] for record in cursor.fetchall()]
    return random.choices(all_uuids, k=quantity)


def iterable_to_gen(iterable):
    for item in iterable:
        yield item


def insert_films(cursor: ps_cursor, conn):
    films_chunk = []
    counter = 1840
    for _ in range(1000):
        tmdb_url = f'https://api.themoviedb.org/3/movie/{counter}?api_key=2bfbae6c0308da5d54b84d37cd087ef8'
        counter += 1

        resp = requests.get(tmdb_url)
        if resp.status_code != 200:
            continue
        data = json.loads(resp.text)
        title = data.get('title')
        description = data.get('overview')
        release_date = data.get('release_date')
        file_path = data.get('homepage')
        _type = random.choice(['movie'])
        imdb_rating = data.get('vote_average')
        genre_names = [x.get('name') for x in data.get('genres')]

        film_uuid = str(uuid.uuid4())
        films_chunk.append((
            datetime.now(),
            None,
            film_uuid,
            title,
            description,
            release_date,
            file_path,
            imdb_rating,
            _type))

        genre_uuids = []
        for genre_name in genre_names:
            cursor.execute(f"select uuid from content.genre where name='{genre_name}'")
            genre_uuid_res = cursor.fetchone()
            if not genre_uuid_res:
                genre_uuid = uuid.uuid4()
                cursor.execute(
                    f"insert into content.genre (created_at, uuid, name, description) values ('{datetime.now()}', '{genre_uuid}', '{genre_name}', '{genre_name}')")
                conn.commit()
                genre_uuids.append(genre_uuid)
            else:
                genre_uuids.append(genre_uuid_res[0])

        film_genre_chunk = [(datetime.now(), str(film_uuid), str(genre_uuid)) for genre_uuid in genre_uuids]
        cursor.executemany("""
                    insert into content.film_genre (created_at, film_uuid, genre_uuid) values (%s, %s, %s)
                    """, film_genre_chunk)

        time.sleep(0.5)

        cursor.executemany("""
        insert into content.film (created_at, updated_at, uuid, title, description, release_date, file_path, imdb_rating, "type") values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, films_chunk)
        films_chunk.clear()

        conn.commit()


def unique_pair_gen(table_1, table_2, quantity):
    user_uuids = get_random_uuids(table_1, quantity)
    film_uuids = get_random_uuids(table_2, quantity)

    unique_pairs = set()
    for u, f in zip(user_uuids, film_uuids):
        unique_pairs.add((u, f))

    while len(unique_pairs) < quantity:
        diff = quantity - len(unique_pairs)
        user_uuids_diff = get_random_uuids(table_1, diff)
        film_uuids_diff = get_random_uuids(table_2, diff)
        unique_pairs_diff = set()
        for u, f in zip(user_uuids_diff, film_uuids_diff):
            unique_pairs_diff.add((u, f))
        unique_pairs.update(unique_pairs_diff)

    return iterable_to_gen(unique_pairs)


FILM_PERSON = 10000
FILM_PERSON_CHUNK = 100


def insert_film_person(cursor, conn):
    person_uuid_film_uuid_gen = unique_pair_gen('content.person', 'content.film', FILM_PERSON)

    film_persons_chunk = []
    for _ in range(FILM_PERSON // FILM_PERSON_CHUNK):
        for _ in range(FILM_PERSON_CHUNK):
            person_uuid, film_uuid = next(person_uuid_film_uuid_gen)
            film_persons_chunk.append(
                (datetime.now(), random.choice(('actor', 'director', 'writer')), film_uuid, person_uuid))

        cursor.executemany("""
                insert into content.film_person (created_at, role, film_uuid, person_uuid)
                values (%s, %s, %s, %s)
                """, film_persons_chunk)
        film_persons_chunk.clear()
        conn.commit()
        print(f'insert_film_person() added {FILM_PERSON_CHUNK}')


if __name__ == '__main__':
    conn = psycopg2.connect(**postgres_config)
    cursor = conn.cursor()

    insert_films(cursor, conn)
    insert_film_person(cursor, conn)

    cursor.close()
    conn.close()
