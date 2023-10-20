# 1) Deploy locally (api at host)
- > make api-redis-build-loc
- > make postgres-build-loc
- > make elastic-build-loc
- > cd api_search && python3.11 -m venv venv && source venv/bin/activate && pip install -r requirements/local.txt
- > export DEBUG=True && export DOCKER=False && python main.py
- swagger docs can be found at 127.0.0.1:8084/docs
- restore there postgres with POST /api/v1/postgres/restore-from-dump choosing file ./api_search_postgres_dump and 'env' = 'local'
- > make django-build-loc
- > make django-superuser-loc
- > make api-etl-postgres-elastic-build-loc
- django admin can be found at 127.0.0.1:88/admin

# 2) Deploy locally (api at docker container)
- > make build-loc
- if some services cant build bcz other unhealthy - try again make build-loc...
- swagger docs can be found at 127.0.0.1:84/docs
- restore there postgres with POST /api/v1/postgres/restore-from-dump choosing file ./api_search_postgres_dump and 'env' = 'docker-compose-local'
- > make api-etl-postgres-elastic-restart-loc
- > make django-superuser-loc
- django admin can be found at 127.0.0.1:88/admin
