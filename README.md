# 1) Run locally
- install docker, docker-compose
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04
-  rename .envs/.example to .envs/.local, set your variables
- > python3.11 -m venv venv
- > source venv/bin/activate && pip install -r api_search/requirements/local.txt && cd api_search/src
- > make build-redis-loc
- > make build-elastic-loc
- > export DEBUG=True
- > export DOCKER=False
- > python main.py

- swagger can be found at 127.0.0.1:8080/[DOCS_URL]

- to run tests locally:
- > pytest

# 2) Run locally in docker-compose
- install docker, docker-compose
-  rename .envs/.example to .envs/.docker-compose-local, set your variables
- > cd api_search/src
- > make build-loc

- swagger can be found at 127.0.0.1/[DOCS_URL]

- to run tests locally in docker-compose:
- > make build-tests-loc


### Соответствие экранов и эндпоинтов
1. Главная страница
- первые 20 самых популярные фильмов по убыванию популярности:
http://127.0.0.1:8080/api/v1/films/?order_by=imdb_rating&order=desc&offset=0&limit=20
- первые 20 фильмов в жанре 'Action' по убыванию популярности:
http://127.0.0.1:8080/api/v1/films/search?order_by=imdb_rating&order=desc&field=genre.name.raw&condition=includes&value=Action&offset=0&limit=20
- список жанров:
http://127.0.0.1:8080/api/v1/genres/

2. Поиск
- первые 20 фильмов c названием содержащим 'Star' по убыванию популярности:
http://127.0.0.1:8080/api/v1/films/search?order_by=imdb_rating&order=desc&field=title.raw&condition=includes&value=Star&offset=0&limit=20
- первые 20 персон с именем содержащим 'Andrew' по возрастанию имени
http://127.0.0.1:8080/api/v1/persons/search?order_by=name.raw&order=asc&field=name.raw&condition=includes&value=Andrew&offset=0&limit=20

3. Страница фильма
http://127.0.0.1:8080/api/v1/films/3b914679-1f5e-4cbd-8044-d13d35d5236c

4. Страница персоны
http://127.0.0.1:8080/api/v1/persons/ed149438-4d76-45c9-861b-d3ed48ccbf0c

5. Страница жанра
http://127.0.0.1:8080/api/v1/genres/3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff

Кэширование
Кэшируются вызовы по отдельным id и query запросы при условии, что offset=0 и limit in (20, 50, 500)