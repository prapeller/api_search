from typing import Any, Dict, List


def transform(rows: List[Dict:Any]):
    """
    Transformer function that morph Postgres-object to ElasticSearch-bulk ready object
    :param rows:
    :return:
    """
    movies = {}
    genres = {}
    persons = {}
    for row in rows:
        _uuid = row[0]
        title = row[1]
        description = row[2]
        imdb_rating = row[3]
        showtype = row[4]
        person_name = row[5]
        person_uuid = row[6]
        role = row[7]
        genre_uuid = row[8]
        genre_name = row[9]

        if genre_uuid not in genres:
            genre = {
                "uuid": genre_uuid,
                "name": genre_name,
                "films": {}
            }
            genres[genre_uuid] = genre

        if person_uuid not in persons:
            person = {
                "uuid": person_uuid,
                "name": person_name,
                "films": {}
            }
            persons[person_uuid] = person

        if _uuid not in movies:
            movie = {
                "uuid": _uuid,
                "title": title,
                "description": description,
                "imdb_rating": imdb_rating,
                "director": {},
                "actor": {},
                "writer": {},
                "genre": {},
                "type": showtype
            }
            movies[_uuid] = movie
        movie = movies[_uuid]
        if person_name and role:
            person = {
                "full_name": person_name,
                "uuid": person_uuid
            }
            if person_uuid not in movie[role.lower()].keys():
                movie[role.lower()][person_uuid] = person
            if _uuid not in persons[person_uuid]['films'].keys():
                persons[person_uuid]['films'][_uuid] = {"uuid": _uuid, "title": title, "imdb_rating": imdb_rating}
        if genre_name:
            genre = {
                "name": genre_name,
                "uuid": genre_uuid
            }
            if genre_name not in movie['genre'].keys():
                movie['genre'][genre_uuid] = genre
            if id not in genres[genre_uuid]['films'].keys():
                genres[genre_uuid]['films'][_uuid] = {"uuid": _uuid, "title": title}

    transformed_movies = [movie for movie in movies.values()]
    transformed_persons = [person for person in persons.values()]
    transformed_genres = [genre for genre in genres.values()]

    return {"movies": transformed_movies, "persons": transformed_persons, "genres": transformed_genres}
