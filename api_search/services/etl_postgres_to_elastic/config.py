import os
from pathlib import Path

import pydantic_settings as ps


class Settings(ps.BaseSettings):
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

    TIMEOUT: int
    STATE_FILENAME: str

    class Config:
        extra = 'allow'

    def __init__(self, DOCKER, DEBUG, BASE_DIR):

        if DEBUG and DOCKER:
            super().__init__(_env_file=[
                BASE_DIR / '.envs/.docker-compose-local/.postgres',
                BASE_DIR / '.envs/.docker-compose-local/.elastic',
            ])
        elif DEBUG and not DOCKER:
            super().__init__(_env_file=[
                BASE_DIR / '.envs/.local/.postgres',
                BASE_DIR / '.envs/.local/.elastic',
            ])
        else:
            super().__init__(_env_file=[
                BASE_DIR / '.envs/.prod/.postgres',
                BASE_DIR / '.envs/.prod/.elastic',
            ])


DEBUG = os.getenv('DEBUG', False) == 'True'
DOCKER = os.getenv('DOCKER', False) == 'True'
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
print(f'{DOCKER=:}, {DEBUG=:}, {BASE_DIR=:}')

settings = Settings(DOCKER, DEBUG, BASE_DIR)
