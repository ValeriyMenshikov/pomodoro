.DEFAULT_GOAL := help

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8081 --reload --env-file .local.env

celery: ## Run the application using celery with provided arguments or defaults
	celery -A worker.celery worker --loglevel=info

celery-flower:
	celery --broker=amqp://guest:guest@localhost:5672// flower --port=5555

grun: ## Run the application using uvicorn with provided arguments or defaults
	gunicorn app.main:app -c gunicorn.conf.py

migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply:
	alembic upgrade head


docker:
	docker compose -f docker-compose.yml up -d --remove-orphans --build

lint:
	poetry run ruff check app --fix
	poetry run black app

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'