up:
	docker compose up -d --build

down:
	docker compose down --remove-orphans

ps:
	docker compose ps

al:
	alembic upgrade heads && cd tests && alembic upgrade heads

main:
	python main.py

venv:
	python3.11 -m venv venv

net:
	docker network create nginx_proxy

5433:
	sudo lsof -i -P -n | grep 5433

8000:
	sudo lsof -i -P -n | grep 8000
