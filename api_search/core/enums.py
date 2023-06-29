from enum import Enum


class EnvEnum(str, Enum):
    local = 'local'
    docker_compose_local = 'docker-compose-local'
    prod = 'prod'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class OrderEnum(str, Enum):
    asc = 'asc'
    desc = 'desc'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class FilterConditionsEnum(str, Enum):
    includes = 'includes'
    lt = 'lt'
    gt = 'gt'
    lte = 'lte'
    gte = 'gte'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class ElasticIndexEnum(str, Enum):
    movies = 'movies'
    genres = 'genres'
    persons = 'persons'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class FilmOrderByEnum(str, Enum):
    id = 'id'
    imdb_rating = 'imdb_rating'
    title = 'title.raw'
    genre = 'genre.name.raw'
    director = 'director.name.raw'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class FilmFilterByEnum(str, Enum):
    id = 'id'
    imdb_rating = 'imdb_rating'
    title = 'title.raw'
    genre = 'genre.name.raw'
    director = 'director.name.raw'
    actors_names = 'actors_names.raw'
    writers_names = 'writers_names.raw'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class GenreOrderByEnum(str, Enum):
    id = 'id'
    name = 'name.raw'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class GenreFilterByEnum(str, Enum):
    id = 'id'
    name = 'name.raw'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class PersonOrderByEnum(str, Enum):
    id = 'id'
    name = 'name.raw'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class PersonFilterByEnum(str, Enum):
    id = 'id'
    name = 'name.raw'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class ResponseDetailEnum(str, Enum):
    films_not_found = 'films not found'
    film_not_found = 'film not found'
    genres_not_found = 'genres not found'
    genre_not_found = 'genre not found'
    persons_not_found = 'persons not found'
    person_not_found = 'person not found'
    another_string = 'another string for using in response detail maybe will be needed in future just for any case'
