export DOCKER_DEFAULT_PLATFORM=linux/amd64

up:
	docker compose -f docker-compose-local.yaml up -d --build

down:
	docker compose -f docker-compose-local.yaml down --remove-orphans

ps:
	docker compose -f docker-compose-local.yaml ps

up_ci:
	docker compose -f docker-compose-ci.yaml up -d

up_ci_rebuild:
	docker compose -f docker-compose-ci.yaml up --build -d

down_ci:
	docker compose -f docker-compose-ci.yaml down --remove-orphans

al:
	alembic upgrade heads && cd tests && alembic upgrade heads

main:
	python main.py
