import pydantic as pd

from db.models.base import IdMixin


class Person(IdMixin):
    name: str


class PersonFilms(Person):
    films: list['FilmReadTitleRating']


class PaginatedPersons(pd.BaseModel):
    total_count: int
    objs: list[Person]


from db.models.film import FilmReadTitleRating

PersonFilms.update_forward_refs()
