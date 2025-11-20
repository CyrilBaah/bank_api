.PHONY: help build up down restart logs shell migrate collectstatic createsuperuser test clean

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker containers
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose restart

logs: ## Show logs for all services
	docker-compose logs -f

logs-app: ## Show logs for Django app only
	docker-compose logs -f app

shell: ## Access Django shell
	docker-compose exec app python manage.py shell

bash: ## Access container bash
	docker-compose exec app bash

migrate: ## Run Django migrations
	docker-compose exec app python manage.py migrate

makemigrations: ## Create Django migrations
	docker-compose exec app python manage.py makemigrations

collectstatic: ## Collect static files
	docker-compose exec app python manage.py collectstatic --noinput

createsuperuser: ## Create Django superuser
	docker-compose exec app python manage.py createsuperuser

test: ## Run tests
	docker-compose exec app python manage.py test

test-services: ## Test all services connectivity
	python test_services.py

dev: build up migrate collectstatic ## Full development setup

clean: ## Remove containers and volumes
	docker-compose down -v
	docker system prune -f

status: ## Show container status
	docker-compose ps
