MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: $(shell egrep -o ^[a-zA-Z_-]+: $(MAKEFILE_LIST) | sed 's/://')

COMPOSE = docker compose -f docker-compose.yml

build:
	@$(COMPOSE) build

start:
	@$(COMPOSE) up -d

stop:
	@$(COMPOSE) down

logs:
	@$(COMPOSE) logs -f

makemigrations:
	@$(COMPOSE) run --rm django python manage.py makemigrations $(app)

migrate:
	@$(COMPOSE) run --rm django python manage.py migrate $(app)

createsuperuser:
	@$(COMPOSE) run --rm django python manage.py createsuperuser

poetry_add:
	@$(COMPOSE) run --rm django poetry add $(name)

startapp:
	@$(COMPOSE) run --rm django python manage.py startapp $(app)

test:
	@$(COMPOSE) run --rm django pytest $(cmd)

coverage:
	@$(COMPOSE) run --rm django coverage run -m pytest
