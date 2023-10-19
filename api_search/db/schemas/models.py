import pydantic as pd


class PersonSerializer(pd.BaseModel):
    id: str
    uuid: str
    name: str


class FilmSerializer(pd.BaseModel):
    id: str
    uuid: str
    imdb_rating: float | None
    genre: list[str] = []
    title: str
    description: str | None
    director: str | None
    actors_names: list[str] = []
    writers_names: list[str] = []
    actors: list[PersonSerializer] = []
    writers: list[PersonSerializer] = []
