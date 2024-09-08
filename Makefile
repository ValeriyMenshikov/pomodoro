.DEFAULT_GOAL := help

run: ## Run the application using uvicorn with provided arguments or defaults
	uvicorn app.main:app --host 0.0.0.0 --port 8081 --reload --env-file .local.env

grun: ## Run the application using uvicorn with provided arguments or defaults
	gunicorn app.main:app -c app/infrastructure/gunicorn.conf.py

migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply:
	alembic upgrade head

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'