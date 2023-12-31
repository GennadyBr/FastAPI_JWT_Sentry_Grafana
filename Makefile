#!/bin/bash

migrate:
	alembic init migrations

#alembic.ini
#sqlalchemy.url = postgresql://postgres:postgres@0.0.0.0:5432/postgres

#env.py
#from main import Base
#target_metadata = Base.metadata

	alembic revision --autogenerate -m "create table for users"
	alembic upgrade head

down:
	docker compose -f docker-compose-local.yaml down
#	docker logs

up:
	docker compose -f docker-compose-local.yaml up -d --build

venv:
	python3.11 -m venv venv
	source venv/bin/activate
