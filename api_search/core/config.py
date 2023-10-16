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

    API_AUTH_HOST: str
    API_AUTH_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    ELASTIC_HOST: str
    ELASTIC_PORT: int

    DOCS_URL: str = 'docs'

    class Config:
        extra = 'allow'

    def __init__(self, DOCKER, DEBUG, BASE_DIR):
        if DEBUG and DOCKER:
            super().__init__(_env_file=[BASE_DIR / '.envs/.docker-compose-local/.api',
                                        BASE_DIR / '.envs/.docker-compose-local/.elastic',
                                        BASE_DIR / '.envs/.docker-compose-local/.redis'])
        elif DEBUG and not DOCKER:
            super().__init__(_env_file=[BASE_DIR / '.envs/.local/.api',
                                        BASE_DIR / '.envs/.local/.elastic',
                                        BASE_DIR / '.envs/.local/.redis'])
        else:
            super().__init__(_env_file=[BASE_DIR / '.envs/.prod/.api',
                                        BASE_DIR / '.envs/.prod/.elastic',
                                        BASE_DIR / '.envs/.prod/.redis'])


DEBUG = True if os.getenv('DEBUG', 'False') == 'True' else False
DOCKER = True if os.getenv('DOCKER', 'False') == 'True' else False
BASE_DIR = Path(__file__).resolve().parent.parent.parent

settings = Settings(DOCKER, DEBUG, BASE_DIR)

ELASTIC_CACHE_EXPIRE_IN_SECONDS: int = 60 * 5
ELASTIC_BACKOFF_MAX_TIME_SEC: int = 500
