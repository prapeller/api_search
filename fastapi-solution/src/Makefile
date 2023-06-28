up:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search up -d

up-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search up -d


build-postgres:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search up --build -d  --remove-orphans --no-deps postgres_search

build-postgres-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search up --build -d  --remove-orphans --no-deps postgres_search


build-redis:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search up --build -d  --remove-orphans --no-deps redis_search

build-redis-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search up --build -d  --remove-orphans --no-deps redis_search


build-elastic:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search up --build -d  --remove-orphans --no-deps elastic_search

build-elastic-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search up --build -d  --remove-orphans --no-deps elastic_search


build-api:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search up --build -d  --remove-orphans --no-deps api_search

build-api-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search up --build -d  --remove-orphans --no-deps api_search


down:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search down

down-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search down


down-v:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search down -v

down-v-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search down -v


restart:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search restart

restart-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search restart


check-config:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search config

check-config-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search config


postgres-dump:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search exec postgres_search dump.sh

postgres-dump-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search exec postgres_search dump.sh


pipinstall:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search run --rm api_search pip install -r requirements/prod.txt

pipinstall-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search run --rm api_search pip install -r requirements/local.txt


check-logs:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search logs

check-logs-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search logs


superuser:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search run --rm api_search python3 -m scripts.create_superuser

superuser-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search run --rm api_search python3 -m scripts.create_superuser


make-migration:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search run --rm api_search python3 -m scripts.make_migration

make-migration-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search run --rm api_search python3 -m scripts.make_migration


migrate:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search run --rm api_search python3 -m scripts.migrate

migrate-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search run --rm api_search python3 -m scripts.migrate


build:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search up --build -d --remove-orphans

build-loc:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search up --build -d --remove-orphans


build-nginx:
	docker-compose -f docker-compose-base.yml -f docker-compose-prod.yml -p project_search up --build -d  --remove-orphans --no-deps nginx


piplist:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search run --rm api_search pip list

flake8:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search exec api_search flake8 .

black-check:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search exec api_search black --check --exclude=venv .

black-diff:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search exec api_search black --diff --exclude=venv .

black:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search exec api_search black --exclude=venv .

isort-check:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search exec api_search isort . --check-only --skip venv

isort-diff:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search exec api_search isort . --diff --skip venv

isort:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search exec api_search isort . --skip venv

tests:
	docker-compose -f docker-compose-base.yml -f docker-compose-local.yml -p project_search up --build -d --remove-orphans --no-deps tests_search




check-vol-media:
	docker volume inspect app_media_volume

check-ip-api:
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' api_search

check-ip-redis:
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis_search
