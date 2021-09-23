ifneq (,$(wildcard ./.env))
	include .env
	export
	ENV_FILE_PATH = --env-file .env
endif

build:
	docker-compose -f docker-compose-dev.yml up --build -d --remove-orphans
	
up:
	docker-compose -f docker-compose-dev.yml up -d

down:
	docker-compose -f docker-compose-dev.yml down

logs:
	docker-compose -f docker-compose-dev.yml logs

migrate:
	docker-compose -f docker-compose-dev.yml exec api python manage.py migrate

makemigrations:
	docker-compose -f docker-compose-dev.yml exec api python manage.py makemigrations

superuser:
	docker-compose -f docker-compose-dev.yml exec api python manage.py createsuperuser

down-v:
	docker-compose -f docker-compose-dev.yml down -v

volume:
	docker volume inspect activo-api_postgres_data

postgres-db:
	docker-compose -f docker-compose-dev.yml exec postgres-db psql --username=$(POSTGRES_USER) --dbname=$(POSTGRES_DB)

test:
	docker-compose -f docker-compose-dev.yml exec api pytest