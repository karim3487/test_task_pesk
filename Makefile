build:
	docker-compose build

up:
	docker-compose up --remove-orphans -d

down:
	docker-compose down

migrate:
	docker-compose exec web uv run manage.py migrate

load_fixtures:
	docker-compose exec web uv run manage.py loaddata authentication/fixtures/users.json