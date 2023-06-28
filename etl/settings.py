from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    dbname: str = Field(..., env='POSTGRES_DB')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field(..., env='POSTGRES_HOST')
    port: str = Field(..., env='POSTGRES_PORT')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class ElasticSettings(BaseSettings):
    host: str = Field(..., env='ELASTIC_HOST')
    port: int = Field(..., env='ELASTIC_PORT')
    index_movies: str = Field(..., env='ELASTIC_MOVIES')
    index_persons: str = Field(..., env='ELASTIC_PERSONS')
    index_genres: str = Field(..., env='ELASTIC_GENRES')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()
    elastic: ElasticSettings = ElasticSettings()
    state_filename: str = Field(..., env='STATE_FILENAME')
    timeout: int = Field(..., env='TIMEOUT')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
