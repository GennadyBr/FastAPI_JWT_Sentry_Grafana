#!/bin/bash

# initial migrations
#alembic init migrations

#alembic.ini
#sqlalchemy.url = postgresql://postgres:postgres@0.0.0.0:5432/postgres

#env.py
#from main import Base
#target_metadata = Base.metadata

#alembic revision --autogenerate -m "create table for users"

docker compose -f docker-compose-local.yaml down
docker compose -f docker-compose-local.yaml up -d --build
alembic upgrade head
#docker logs
