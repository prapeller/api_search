API_SEARCH_LOCAL := -p api_search -f ./docker/api/docker-compose-local.yml
ELASTIC_SEARCH_LOCAL := -p elastic_search -f ./docker/elastic/docker-compose-local.yml
POSTGRES_SEARCH_LOCAL := -p postgres_search -f ./docker/postgres/docker-compose-local.yml
DJANGO_SEARCH_LOCAL := -p django_search -f ./docker/django/docker-compose-local.yml

API_SEARCH_PROD := -p api_search -f ./docker/api/docker-compose-prod.yml
ELASTIC_SEARCH_PROD := -p elastic_search -f ./docker/elastic/docker-compose-prod.yml
POSTGRES_SEARCH_PROD := -p postgres_search -f ./docker/postgres/docker-compose-prod.yml
DJANGO_SEARCH_PROD := -p django_search -f ./docker/django/docker-compose-prod.yml

build-loc:
	@docker network create shared_network || true
	docker-compose $(POSTGRES_SEARCH_LOCAL) up --build -d --remove-orphans
	docker-compose $(ELASTIC_SEARCH_LOCAL) up --build -d --remove-orphans
	docker-compose $(API_SEARCH_LOCAL) up --build -d --remove-orphans
	docker-compose $(DJANGO_SEARCH_LOCAL) up --build -d --remove-orphans

build:
	@docker network create shared_network || true
	docker-compose $(POSTGRES_SEARCH_PROD) up --build -d --remove-orphans
	docker-compose $(ELASTIC_SEARCH_PROD) up --build -d --remove-orphans
	docker-compose $(API_SEARCH_PROD) up --build -d --remove-orphans
	docker-compose $(DJANGO_SEARCH_PROD) up --build -d --remove-orphans

down-loc:
	docker-compose $(POSTGRES_SEARCH_LOCAL) down
	docker-compose $(ELASTIC_SEARCH_LOCAL) down
	docker-compose $(API_SEARCH_LOCAL) down
	docker-compose $(DJANGO_SEARCH_LOCAL) down

down:
	docker-compose $(POSTGRES_SEARCH_PROD) down
	docker-compose $(ELASTIC_SEARCH_PROD) down
	docker-compose $(API_SEARCH_PROD) down
	docker-compose $(DJANGO_SEARCH_PROD) down

down-v-loc:
	docker-compose $(POSTGRES_SEARCH_LOCAL) down -v
	docker-compose $(ELASTIC_SEARCH_LOCAL) down -v
	docker-compose $(API_SEARCH_LOCAL) down -v
	docker-compose $(DJANGO_SEARCH_LOCAL) down -v

down-v:
	docker-compose $(POSTGRES_SEARCH_PROD) down -v
	docker-compose $(ELASTIC_SEARCH_PROD) down -v
	docker-compose $(API_SEARCH_PROD) down -v
	docker-compose $(DJANGO_SEARCH_PROD) down -v


api-build-loc:
	docker-compose $(API_SEARCH_LOCAL) up --build -d  --remove-orphans --no-deps api_search

api-build:
	docker-compose $(API_SEARCH_PROD) up --build -d  --remove-orphans --no-deps api_search

api-pipinstall-loc:
	docker-compose $(API_SEARCH_LOCAL)  run --rm api_search pip install -r requirements/local.txt

api-pipinstall:
	docker-compose $(API_SEARCH_PROD)  run --rm api_search pip install -r requirements/prod.txt

api-check-ip:
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' api_search

api-etl-postgres-elastic-build-loc:
	docker-compose $(API_SEARCH_LOCAL) up --build -d --remove-orphans --no-deps etl_postgres_to_elastic_search

api-redis-build-loc:
	docker-compose $(API_SEARCH_LOCAL) up --build -d --remove-orphans --no-deps redis_search

api-tests-build-loc:
	docker-compose $(API_SEARCH_LOCAL) up --build -d --remove-orphans --no-deps tests_search

api-create-superuser-loc:
	docker-compose $(API_SEARCH_LOCAL) run --rm api_search python3 -m scripts.create_superuser

api-create-superuser:
	docker-compose $(API_SEARCH_PROD) run --rm api_search python3 -m scripts.create_superuser

api-make-migration-loc:
	docker-compose $(API_SEARCH_LOCAL) run --rm api_search python3 -m scripts.make_migration

api-make-migration:
	docker-compose $(API_SEARCH_PROD) run --rm api_search python3 -m scripts.make_migration

api-migrate-loc:
	docker-compose $(API_SEARCH_LOCAL) run --rm api_search python3 -m scripts.migrate

api-migrate:
	docker-compose $(API_SEARCH_PROD) run --rm api_search python3 -m scripts.migrate



django-build-loc:
	docker-compose $(DJANGO_SEARCH_LOCAL) up --build -d  --remove-orphans --no-deps

django-build:
	docker-compose $(DJANGO_SEARCH_PROD) up --build -d  --remove-orphans --no-deps

django-down-loc:
	docker-compose $(DJANGO_SEARCH_LOCAL) down

django-down:
	docker-compose $(DJANGO_SEARCH_PROD) down

django-down-v-loc:
	docker-compose $(DJANGO_SEARCH_LOCAL) down -v

django-down-v:
	docker-compose $(DJANGO_SEARCH_PROD) down -v

django-superuser-loc:
	docker-compose $(DJANGO_SEARCH_LOCAL) run --rm django_search python3 manage.py createsuperuser

django-superuser:
	docker-compose $(DJANGO_SEARCH_PROD) run --rm django_search python3 manage.py createsuperuser

django-migrate-loc:
	docker-compose $(DJANGO_SEARCH_LOCAL) run --rm django_search python3 manage.py migrate

django-migrate:
	docker-compose $(DJANGO_SEARCH_PROD) run --rm django_search python3 manage.py migrate

django-make-migration-loc:
	docker-compose $(DJANGO_SEARCH_LOCAL) run --rm django_search python3 manage.py makemigrations

django-make-migration:
	docker-compose $(DJANGO_SEARCH_PROD) run --rm django_search python3 manage.py makemigrations

django-collectstatic-loc:
	docker-compose $(DJANGO_SEARCH_LOCAL) run --rm django_search python3 manage.py collectstatic --no-input --clear

django-collectstatic:
	docker-compose $(DJANGO_SEARCH_PROD) run --rm django_search python3 manage.py collectstatic --no-input --clear

django-shell-loc:
	docker-compose $(DJANGO_SEARCH_LOCAL) run --rm django_search python3 manage.py shell

django-shell:
	docker-compose $(DJANGO_SEARCH_PROD) run --rm django_search python3 manage.py shell

django-shell-plus-loc:
	docker-compose $(DJANGO_SEARCH_LOCAL) run --rm django_search python3 manage.py shell_plus --plain

django-shell-plus:
	docker-compose $(DJANGO_SEARCH_PROD) run --rm django_search python3 manage.py shell_plus --plain

django-shell-plus-sql-loc:
	docker-compose $(DJANGO_SEARCH_LOCAL) run --rm django_search python3 manage.py shell_plus --print-sql

django-shell-plus-sql:
	docker-compose $(DJANGO_SEARCH_PROD) run --rm django_search python3 manage.py shell_plus --print-sql

django-rebuild-index-loc:
	docker-compose $(DJANGO_SEARCH_LOCAL) run --rm django_search python3 manage.py rebuild_index

django-rebuild-index:
	docker-compose $(DJANGO_SEARCH_PROD) run --rm django_search python3 manage.py rebuild_index



postgres-build-loc:
	docker-compose $(POSTGRES_SEARCH_LOCAL) up --build -d  --remove-orphans --no-deps postgres_search

postgres-build:
	docker-compose $(POSTGRES_SEARCH_PROD) up --build -d  --remove-orphans --no-deps postgres_search

postgres-build-loc:
	docker-compose $(POSTGRES_SEARCH_LOCAL) up --build -d  --remove-orphans --no-deps postgres_search

postgres-build:
	docker-compose $(POSTGRES_SEARCH_PROD) up --build -d  --remove-orphans --no-deps postgres_search

postgres-down-loc:
	docker-compose $(POSTGRES_SEARCH_LOCAL) down

postgres-down:
	docker-compose $(POSTGRES_SEARCH_PROD) down

postgres-down-v-loc:
	docker-compose $(POSTGRES_SEARCH_LOCAL) down -v

postgres-down-v:
	docker-compose $(POSTGRES_SEARCH_PROD) down -v

postgres-dump-loc:
	docker-compose $(POSTGRES_SEARCH_LOCAL) exec postgres_search dump.sh

postgres-dump:
	docker-compose $(POSTGRES_SEARCH_PROD) exec postgres_search dump.sh



elastic-build:
	docker-compose $(ELASTIC_SEARCH_PROD)  up --build -d  --remove-orphans --no-deps elastic_search

elastic-build-loc:
	docker-compose $(ELASTIC_SEARCH_LOCAL)  up --build -d  --remove-orphans --no-deps elastic_search

elastic-down:
	docker-compose $(ELASTIC_SEARCH_PROD) down

elastic-down-loc:
	docker-compose $(ELASTIC_SEARCH_LOCAL) down

elastic-down-v:
	docker-compose $(ELASTIC_SEARCH_PROD) down -v

elastic-down-v-loc:
	docker-compose $(ELASTIC_SEARCH_LOCAL) down -v



check-config:
	docker-compose $(API_SEARCH_PROD) config

check-config-loc:
	docker-compose $(API_SEARCH_LOCAL) config



check-logs:
	docker-compose $(API_SEARCH_PROD) logs

check-logs-loc:
	docker-compose $(API_SEARCH_LOCAL) logs



nginx-build:
	docker-compose $(API_SEARCH_PROD) up --build -d  --remove-orphans --no-deps nginx



flake8:
	docker-compose $(API_SEARCH_LOCAL) exec api_search flake8 .

black-check:
	docker-compose $(API_SEARCH_LOCAL) exec api_search black --check --exclude=venv .

black-diff:
	docker-compose $(API_SEARCH_LOCAL) exec api_search black --diff --exclude=venv .

black:
	docker-compose $(API_SEARCH_LOCAL) exec api_search black --exclude=venv .

isort-check:
	docker-compose $(API_SEARCH_LOCAL) exec api_search isort . --check-only --skip venv

isort-diff:
	docker-compose $(API_SEARCH_LOCAL) exec api_search isort . --diff --skip venv

isort:
	docker-compose $(API_SEARCH_LOCAL) exec api_search isort . --skip venv
