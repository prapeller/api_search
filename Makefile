API_DOCKER_COMPOSE_LOCAL := -p api_search -f ./docker/api/docker-compose-local.yml
ELASTIC_DOCKER_COMPOSE_LOCAL := -p elastic_search -f ./docker/elastic/docker-compose-local.yml
POSTGRES_DOCKER_COMPOSE_LOCAL := -p postgres_search -f ./docker/postgres/docker-compose-local.yml
API_DOCKER_COMPOSE_PROD := -p api_search -f ./docker/api/docker-compose-prod.yml

build-loc:
	@docker network create shared_network || true
	docker-compose $(POSTGRES_DOCKER_COMPOSE_LOCAL) up --build -d --remove-orphans
	docker-compose $(ELASTIC_DOCKER_COMPOSE_LOCAL) up --build -d --remove-orphans
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) up --build -d --remove-orphans

down-loc:
	docker-compose $(POSTGRES_DOCKER_COMPOSE_LOCAL) down
	docker-compose $(ELASTIC_DOCKER_COMPOSE_LOCAL) down
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) down

down-v-loc:
	docker-compose $(POSTGRES_DOCKER_COMPOSE_LOCAL) down -v
	docker-compose $(ELASTIC_DOCKER_COMPOSE_LOCAL) down -v
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) down -v

build:
	@docker network create shared_network || true
	docker-compose $(POSTGRES_DOCKER_COMPOSE_PROD) up --build -d --remove-orphans
	docker-compose $(ELASTIC_DOCKER_COMPOSE_PROD) up --build -d --remove-orphans
	docker-compose $(API_DOCKER_COMPOSE_PROD) up --build -d --remove-orphans

down:
	docker-compose $(POSTGRES_DOCKER_COMPOSE_PROD) down
	docker-compose $(ELASTIC_DOCKER_COMPOSE_PROD) down
	docker-compose $(API_DOCKER_COMPOSE_PROD) down

down-v:
	docker-compose $(POSTGRES_DOCKER_COMPOSE_PROD) down -v
	docker-compose $(ELASTIC_DOCKER_COMPOSE_PROD) down -v
	docker-compose $(API_DOCKER_COMPOSE_PROD) down -v



api-build:
	docker-compose $(API_DOCKER_COMPOSE_PROD) up --build -d  --remove-orphans --no-deps api_search

api-build-loc:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) up --build -d  --remove-orphans --no-deps api_search

api-pipinstall:
	docker-compose $(API_DOCKER_COMPOSE_PROD)  run --rm api_search pip install -r requirements/prod.txt

api-pipinstall-loc:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL)  run --rm api_search pip install -r requirements/local.txt

api-check-ip:
	docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' api_search

api-etl-postgres-elastic-build-loc:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) up --build -d --remove-orphans --no-deps etl_postgres_to_elastic_search

api-redis-build-loc:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) up --build -d --remove-orphans --no-deps redis_search

api-tests-build-loc:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) up --build -d --remove-orphans --no-deps tests_search


postgres-build:
	docker-compose $(POSTGRES_DOCKER_COMPOSE_PROD) up --build -d  --remove-orphans --no-deps postgres_search

postgres-build-loc:
	docker-compose $(POSTGRES_DOCKER_COMPOSE_LOCAL) up --build -d  --remove-orphans --no-deps postgres_search

postgres-dump:
	docker-compose $(POSTGRES_DOCKER_COMPOSE_PROD) exec postgres_search dump.sh

postgres-dump-loc:
	docker-compose $(POSTGRES_DOCKER_COMPOSE_LOCAL) exec postgres_search dump.sh



elastic-build:
	docker-compose $(ELASTIC_DOCKER_COMPOSE_PROD)  up --build -d  --remove-orphans --no-deps elastic_search

elastic-build-loc:
	docker-compose $(ELASTIC_DOCKER_COMPOSE_LOCAL)  up --build -d  --remove-orphans --no-deps elastic_search



check-config:
	docker-compose $(API_DOCKER_COMPOSE_PROD) config

check-config-loc:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) config



check-logs:
	docker-compose $(API_DOCKER_COMPOSE_PROD) logs

check-logs-loc:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) logs


superuser:
	docker-compose $(API_DOCKER_COMPOSE_PROD) run --rm api_search python3 -m scripts.create_superuser

superuser-loc:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) run --rm api_search python3 -m scripts.create_superuser


make-migration:
	docker-compose $(API_DOCKER_COMPOSE_PROD) run --rm api_search python3 -m scripts.make_migration

make-migration-loc:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) run --rm api_search python3 -m scripts.make_migration


migrate:
	docker-compose $(API_DOCKER_COMPOSE_PROD) run --rm api_search python3 -m scripts.migrate

migrate-loc:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) run --rm api_search python3 -m scripts.migrate



nginx-build:
	docker-compose $(API_DOCKER_COMPOSE_PROD) up --build -d  --remove-orphans --no-deps nginx



flake8:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) exec api_search flake8 .

black-check:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) exec api_search black --check --exclude=venv .

black-diff:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) exec api_search black --diff --exclude=venv .

black:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) exec api_search black --exclude=venv .

isort-check:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) exec api_search isort . --check-only --skip venv

isort-diff:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) exec api_search isort . --diff --skip venv

isort:
	docker-compose $(API_DOCKER_COMPOSE_LOCAL) exec api_search isort . --skip venv
