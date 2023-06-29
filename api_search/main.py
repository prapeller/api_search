import elasticsearch as es
import fastapi as fa
import uvicorn
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

import core.dependencies
from api.v1 import postgres as v1_postgres
from api.v1.films import FilmsRouterV1
from api.v1.genres import GenresRouterV1
from api.v1.persons import PersonsRouterV1
from core.config import settings
from core.dependencies import verified_access_token_dependency

app = fa.FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=f'/{settings.DOCS_URL}',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    core.dependencies.redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    core.dependencies.es = es.AsyncElasticsearch(hosts=[f'http://{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}'])


@app.on_event('shutdown')
async def shutdown():
    await core.dependencies.redis.close()
    await core.dependencies.es.close()


v1_router = fa.APIRouter(
    dependencies=[fa.Depends(verified_access_token_dependency)]
)
v1_router.include_router(FilmsRouterV1().router, prefix='/films', tags=['films'])
v1_router.include_router(GenresRouterV1().router, prefix='/genres', tags=['genres'])
v1_router.include_router(PersonsRouterV1().router, prefix='/persons', tags=['persons'])
v1_router.include_router(v1_postgres.router, prefix='/postgres', tags=['postgres'])

app.include_router(v1_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run('main:app', host=settings.API_HOST, port=settings.API_PORT, reload=True)
