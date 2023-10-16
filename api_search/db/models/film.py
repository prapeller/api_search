import pydantic as pd

from db.models.base import IdMixin


class Film(IdMixin):
    title: str
    description: str
    director: list['Person']
    actors_names: list[str]
    writers_names: list[str]
    actors: list['Person']
    writers: list['Person']
    genre: list['Genre']
    imdb_rating: float | None


class FilmReadTitleRating(IdMixin):
    title: str
    imdb_rating: float | None


class PaginatedFilmsReadTitleRating(pd.BaseModel):
    total_count: int
    objs: list[FilmReadTitleRating]


from db.models.person import Person
from db.models.genre import Genre

Film.model_rebuild()
