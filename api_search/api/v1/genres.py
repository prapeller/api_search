from api.v1.shared import Router
from core.dependencies import (
    genre_filter_params_dependency,
    es_service_genre_dependency
)
from core.enums import ResponseDetailEnum, GenreOrderByEnum
from db.models.genre import Genre, PaginatedGenres


class GenresRouterV1(Router):
    def __init__(self):
        super().__init__(
            order_by_enum=GenreOrderByEnum,
            order_by_default=GenreOrderByEnum.name,
            filter_params_dependency=genre_filter_params_dependency,
            search_service_dependency=es_service_genre_dependency,
            objs_not_found_detail=ResponseDetailEnum.genres_not_found,
            obj_not_found_detail=ResponseDetailEnum.genre_not_found,
            obj_response_model=Genre,
            paginated_objs_response_model=PaginatedGenres
        )
        self.list()
        self.list_search()
        self.get_by_id()
