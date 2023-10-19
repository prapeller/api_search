import os
from logging import config as logging_config
from pathlib import Path

import pydantic_settings as ps

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(ps.BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    ELASTIC_HOST: str
    ELASTIC_PORT: int

    class Config:
        extra = 'allow'

    def __init__(self, DOCKER, DEBUG, BASE_DIR):
        if DEBUG and DOCKER:
            super().__init__(_env_file=[BASE_DIR / '.envs/.docker-compose-local/.postgres',
                                        BASE_DIR / '.envs/.docker-compose-local/.elastic',
                                        ])
        elif DEBUG and not DOCKER:
            super().__init__(_env_file=[BASE_DIR / '.envs/.local/.postgres',
                                        BASE_DIR / '.envs/.local/.elastic',
                                        ])
        else:
            super().__init__(_env_file=[BASE_DIR / '.envs/.prod/.postgres',
                                        BASE_DIR / '.envs/.prod/.elastic',
                                        ])


DEBUG = True if os.getenv('DEBUG', 'False') == 'True' else False
DOCKER = True if os.getenv('DOCKER', 'False') == 'True' else False
BASE_DIR = Path(__file__).resolve().parent.parent

settings = Settings(DOCKER, DEBUG, BASE_DIR)

ELASTIC_CACHE_EXPIRE_IN_SECONDS: int = 60 * 5
ELASTIC_BACKOFF_MAX_TIME_SEC: int = 500
