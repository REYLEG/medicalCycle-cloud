.PHONY: help install dev test lint format clean docker-up docker-down

help:
	@echo "MedicalCycle Cloud - Backend Development Commands"
	@echo ""
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@echo "  install       Install dependencies"
	@echo "  dev           Run development server"
	@echo "  test          Run tests"
	@echo "  test-cov      Run tests with coverage"
	@echo "  lint          Run linters (flake8, mypy)"
	@echo "  format        Format code (black, isort)"
	@echo "  clean         Clean up temporary files"
	@echo "  docker-up     Start Docker containers"
	@echo "  docker-down   Stop Docker containers"
	@echo "  docker-logs   View Docker logs"
	@echo "  init-db       Initialize database"

install:
	cd backend && pip install -r requirements-dev.txt

dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	cd backend && pytest

test-cov:
	cd backend && pytest --cov=app --cov-report=html

lint:
	cd backend && flake8 app tests && mypy app

format:
	cd backend && black app tests && isort app tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f backend

init-db:
	cd backend && python -m app.db.init_db
