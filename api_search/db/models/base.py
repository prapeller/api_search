from uuid import UUID, uuid4

import orjson
import pydantic as pd


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class IdMixin(pd.BaseModel):
    id: UUID = pd.Field(default_factory=uuid4)

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
