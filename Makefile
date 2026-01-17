# Makefile for GuardianAI project

# Variables
PYTHON = python3
PIP = pip
DOCKER = docker
DOCKER_COMPOSE = docker-compose

# Default target
.PHONY: help
help:
	@echo "GuardianAI Development Commands"
	@echo "=============================="
	@echo "setup-dev     - Set up development environment"
	@echo "run-backend   - Run backend server"
	@echo "run-frontend  - Run frontend development server"
	@echo "run-all       - Run all services with Docker Compose"
	@echo "test          - Run all tests"
	@echo "test-backend  - Run backend tests"
	@echo "lint          - Run code linting"
	@echo "format        - Format code with Black"
	@echo "docs          - Build and serve documentation"
	@echo "clean         - Clean Python cache files"

# Set up development environment
.PHONY: setup-dev
setup-dev:
	$(PIP) install -r requirements.txt
	cd backend && $(PIP) install -r requirements.txt
	cd docs && $(PIP) install -r requirements.txt

# Run backend server
.PHONY: run-backend
run-backend:
	cd backend && uvicorn main:app --reload

# Run all services with Docker Compose
.PHONY: run-all
run-all:
	$(DOCKER_COMPOSE) up --build

# Run all tests
.PHONY: test
test:
	$(PYTHON) -m pytest tests/ -v

# Run backend tests
.PHONY: test-backend
test-backend:
	cd backend && $(PYTHON) -m pytest tests/ -v

# Run code linting
.PHONY: lint
lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m black --check .

# Format code with Black
.PHONY: format
format:
	$(PYTHON) -m black .

# Build and serve documentation
.PHONY: docs
docs:
	cd docs && mkdocs serve

# Clean Python cache files
.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist

# Install project in development mode
.PHONY: install
install:
	$(PIP) install -e .

# Create database migrations (placeholder)
.PHONY: migrate
migrate:
	@echo "Database migration functionality would be implemented here"

# Backup database (placeholder)
.PHONY: backup
backup:
	@echo "Database backup functionality would be implemented here"