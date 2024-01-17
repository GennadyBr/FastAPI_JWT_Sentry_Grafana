up:
	docker compose up -d --build

down:
	docker compose down --remove-orphans

ps:
	docker compose ps

main:
	python main.py
