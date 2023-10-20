import os
from logging import config as logging_config
from pathlib import Path

import pydantic_settings as ps

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(ps.BaseSettings):
    PROJECT_NAME: str

    API_SEARCH_HOST: str
    API_SEARCH_PORT: int
    DOCS_URL: str = 'docs'

    API_AUTH_HOST: str
    API_AUTH_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    ELASTIC_HOST: str
    ELASTIC_PORT: int
    ELASTIC_MOVIES: str
    ELASTIC_PERSONS: str
    ELASTIC_GENRES: str

    ETL_LOOP_SLEEP_SECONDS: int
    ETL_STATE_FILENAME: str

    class Config:
        extra = 'allow'

    def __init__(self, DOCKER, DEBUG, BASE_DIR):
        if DEBUG and DOCKER:
            super().__init__(_env_file=[BASE_DIR / '.envs/.docker-compose-local/.api',
                                        BASE_DIR / '.envs/.docker-compose-local/.elastic',
                                        BASE_DIR / '.envs/.docker-compose-local/.postgres',
                                        BASE_DIR / '.envs/.docker-compose-local/.redis'])
        elif DEBUG and not DOCKER:
            super().__init__(_env_file=[BASE_DIR / '.envs/.local/.api',
                                        BASE_DIR / '.envs/.local/.elastic',
                                        BASE_DIR / '.envs/.local/.postgres',
                                        BASE_DIR / '.envs/.local/.redis'])
        else:
            super().__init__(_env_file=[BASE_DIR / '.envs/.prod/.api',
                                        BASE_DIR / '.envs/.prod/.elastic',
                                        BASE_DIR / '.envs/.prod/.postgres',
                                        BASE_DIR / '.envs/.prod/.redis'])


DEBUG = True if os.getenv('DEBUG', 'False') == 'True' else False
DOCKER = True if os.getenv('DOCKER', 'False') == 'True' else False
BASE_DIR = Path(__file__).resolve().parent.parent.parent

settings = Settings(DOCKER, DEBUG, BASE_DIR)

ELASTIC_BACKOFF_MAX_TIME_SEC: int = 500
REDIS_CACHE_EXPIRES_IN_SECONDS: int = 30
