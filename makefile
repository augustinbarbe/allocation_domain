PSQL = psql
DATABASE = postgres
PASSWORD = password
HOST = 0.0.0.0
USER = postgres

.PHONY: clean run build test

default: run

build:
	@docker compose build

install:
		pip install tox	

test: export ENV = test
test: install
		tox -- --cov=app tests/ --cov-report xml --cov-report term

run: export ENV=dev
run:
	@echo "Starting stack"
	@docker compose up -d --build

attach:
	@docker attach "$(docker ps -q -f name=api | head -1)"

psql-start-db:
	@docker run -p 5432:5432 --rm --name reference_database -e POSTGRES_PASSWORD=password -d postgres

psql-stop-db:
	@docker stop reference_database

psql-create-db:
	@echo "creating db"
	@echo "CREATE DATABASE ${DATABASE};" |PGPASSWORD=$(PASSWORD) $(PSQL) -h $(HOST) -U $(USER) -d postgres

delete-version:
	@echo "Cleaning migration/versions folder"
	@rm -rf migrations/versions/*

initial-version: export SQLALCHEMY_DATABASE_URI=postgresql://$(USER):$(PASSWORD)@$(HOST):5432/$(DATABASE)
initial-version: delete-version
	@echo "Generating initial migration"
	@echo $(SQLALCHEMY_DATABASE_URI)
	@alembic revision -m "initial schema" --autogenerate 

reinit-schema: psql-create-db initial-version


clean : export ENV=dev
clean : 
	@docker compose down

