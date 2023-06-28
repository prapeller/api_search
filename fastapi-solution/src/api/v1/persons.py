from api.v1.shared import Router
from core.dependencies import (person_filter_params_dependency,
                               es_service_person_dependency)
from core.enums import PersonOrderByEnum
from core.enums import ResponseDetailEnum
from db.models.person import PersonFilms, PaginatedPersons


class PersonsRouterV1(Router):
    def __init__(self):
        super().__init__(
            order_by_enum=PersonOrderByEnum,
            order_by_default=PersonOrderByEnum.name,
            filter_params_dependency=person_filter_params_dependency,
            search_service_dependency=es_service_person_dependency,
            objs_not_found_detail=ResponseDetailEnum.persons_not_found,
            obj_not_found_detail=ResponseDetailEnum.person_not_found,
            obj_response_model=PersonFilms,
            paginated_objs_response_model=PaginatedPersons
        )
        self.list()
        self.list_search()
        self.get_by_id()
