import uuid
from enum import Enum

import fastapi as fa
import pydantic as pd

from core.dependencies import pagination_params_dependency
from core.enums import OrderEnum
from services.searchservice import SearchService


class Router:
    order_by_enum: Enum | None
    order_by_default: str
    filter_params_dependency: fa.Depends
    search_service_dependency: fa.Depends
    objs_not_found_detail: str
    obj_not_found_detail: str
    paginated_objs_response_model: type[pd.BaseModel]
    obj_response_model: type[pd.BaseModel]

    def list(self):
        @self.router.get('/', response_model=self.paginated_objs_response_model)
        async def list_items(
                order_by: Router.order_by_enum = self.order_by_default,
                order: OrderEnum = OrderEnum.desc,
                pagination_params: dict = fa.Depends(pagination_params_dependency),
                search_service: SearchService = fa.Depends(self.search_service_dependency),
        ):
            must_be_ordered = not any(param is None for param in (order_by, order))
            if must_be_ordered:
                await search_service.order(order_by=order_by, order=order)
            await search_service.limit_offset(limit=pagination_params['limit'], offset=pagination_params['offset'])
            objs = await search_service.search()
            if not objs:
                raise fa.HTTPException(status_code=fa.status.HTTP_404_NOT_FOUND,
                                       detail=self.objs_not_found_detail)
            paginated_objs = self.paginated_objs_response_model(total_count=await search_service.count(), objs=objs)
            return paginated_objs

    def list_search(self):
        @self.router.get('/search', response_model=self.paginated_objs_response_model)
        async def list_items_search(
                order_by: Router.order_by_enum = self.order_by_default,
                filter_params: dict = fa.Depends(self.filter_params_dependency),
                order: OrderEnum = OrderEnum.asc,
                pagination_params: dict = fa.Depends(pagination_params_dependency),
                search_service: SearchService = fa.Depends(self.search_service_dependency),
        ):
            must_be_ordered = not any(param is None for param in (order_by, order))
            must_be_filtered = not (not filter_params
                                    or any(param_value is None for param_key, param_value in filter_params.items()))
            if must_be_filtered:
                await search_service.filter(**filter_params)
            if must_be_ordered:
                await search_service.order(order_by=order_by, order=order)
            await search_service.limit_offset(limit=pagination_params['limit'], offset=pagination_params['offset'])
            objs = await search_service.search()
            if not objs:
                raise fa.HTTPException(status_code=fa.status.HTTP_404_NOT_FOUND, detail=self.objs_not_found_detail)
            paginated_objs = self.paginated_objs_response_model(total_count=await search_service.count(), objs=objs)
            return paginated_objs

    def get_by_id(self):
        @self.router.get('/{uuid}', response_model=self.obj_response_model)
        async def get_item_by_id(
                uuid: pd.UUID4,
                search_service=fa.Depends(self.search_service_dependency),
        ):
            obj = await search_service.get_by_uuid(str(uuid))
            if not obj:
                raise fa.HTTPException(status_code=fa.status.HTTP_404_NOT_FOUND, detail=self.obj_not_found_detail)
            return obj

    def __init__(self,
                 order_by_enum,
                 order_by_default,
                 filter_params_dependency,
                 search_service_dependency,
                 objs_not_found_detail,
                 obj_not_found_detail,
                 obj_response_model,
                 paginated_objs_response_model,
                 ):
        self.router = fa.APIRouter()

        Router.order_by_enum = order_by_enum
        self.order_by_default = order_by_default
        self.filter_params_dependency = filter_params_dependency
        self.search_service_dependency = search_service_dependency
        self.objs_not_found_detail = objs_not_found_detail
        self.obj_not_found_detail = obj_not_found_detail
        self.obj_response_model = obj_response_model
        self.paginated_objs_response_model = paginated_objs_response_model
