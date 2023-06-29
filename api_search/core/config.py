import os
from logging import config as logging_config
from pathlib import Path

import pydantic as pd

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(pd.BaseSettings):
    PROJECT_NAME: str = 'movies'

    API_HOST: str = '127.0.0.1'
    API_PORT: int = 8081

    AUTH_API_HOST: str = '127.0.0.1'
    AUTH_API_PORT: int = 8080

    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379

    ELASTIC_HOST: str = '127.0.0.1'
    ELASTIC_PORT: int = 9200

    DOCS_URL: str = 'docs'

    ELASTIC_CACHE_EXPIRE_IN_SECONDS: int = 60 * 5
    ELASTIC_BACKOFF_MAX_TIME_SEC: int = 500

    def __init__(self, DOCKER, DEBUG):
        BASE_DIR = Path(__file__).resolve().parent.parent

        if DEBUG and DOCKER:
            super().__init__([BASE_DIR / '.envs/.docker-compose-local/.api',
                              BASE_DIR / '.envs/.docker-compose-local/.elastic',
                              BASE_DIR / '.envs/.docker-compose-local/.redis'])
        elif DEBUG and not DOCKER:
            super().__init__([BASE_DIR / '.envs/.local/.api',
                              BASE_DIR / '.envs/.local/.elastic',
                              BASE_DIR / '.envs/.local/.redis'])
        else:
            super().__init__([BASE_DIR / '.envs/.prod/.api',
                              BASE_DIR / '.envs/.prod/.elastic',
                              BASE_DIR / '.envs/.prod/.redis'])


DEBUG = True if os.getenv('DEBUG', 'False') == 'True' else False
DOCKER = True if os.getenv('DOCKER', 'False') == 'True' else False

settings = Settings(DOCKER, DEBUG)
