import pydantic as pd

from db.models.base import IdMixin


class Genre(IdMixin):
    name: str


class PaginatedGenres(pd.BaseModel):
    total_count: int
    objs: list[Genre]
