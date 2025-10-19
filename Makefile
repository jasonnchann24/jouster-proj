# Django Docker Development Makefile

env-init:
	cp envs/.env.example envs/.env
	cp envs/.env.api.example envs/.env.api

# Docker commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

# Container access
react:
	docker-compose exec react sh

django:
	docker-compose exec django bash

cp-envs: env-init

install: build up migrate
# Django management commands
migrate:
	docker-compose exec django python3 manage.py migrate

test:
	docker-compose exec django python3 manage.py test

# Utility commands
restart: down up

clean:
	docker-compose down -v --remove-orphans
	docker system prune -f
