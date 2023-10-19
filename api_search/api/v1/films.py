from api.v1.shared import Router
from core.dependencies import (
    film_filter_params_dependency,
    es_service_film_dependency,
)
from core.enums import FilmOrderByEnum, ResponseDetailEnum
from db.models.film import Film, PaginatedFilmsReadTitleRating


class FilmsRouterV1(Router):
    def __init__(self):
        super().__init__(
            order_by_enum=FilmOrderByEnum,
            order_by_default=FilmOrderByEnum.imdb_rating,
            filter_params_dependency=film_filter_params_dependency,
            search_service_dependency=es_service_film_dependency,
            objs_not_found_detail=ResponseDetailEnum.films_not_found,
            obj_not_found_detail=ResponseDetailEnum.film_not_found,
            obj_response_model=Film,
            paginated_objs_response_model=PaginatedFilmsReadTitleRating
        )
        self.list()
        self.list_search()
        self.get_by_id()
