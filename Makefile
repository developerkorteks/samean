# KortekStream API Makefile

.PHONY: help build start stop restart logs status clean dev prod

# Default target
help:
	@echo "KortekStream API - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make dev        - Start development environment"
	@echo "  make build      - Build Docker images"
	@echo "  make start      - Start services"
	@echo "  make stop       - Stop services"
	@echo "  make restart    - Restart services"
	@echo "  make logs       - Show logs"
	@echo "  make status     - Show service status"
	@echo ""
	@echo "Production:"
	@echo "  make prod       - Start production environment"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean      - Clean up containers and images"
	@echo "  make test       - Test API endpoints"
	@echo ""

# Development commands
dev: build start

build:
	@echo "Building Docker images..."
	@./deploy.sh build

start:
	@echo "Starting services..."
	@./deploy.sh start

stop:
	@echo "Stopping services..."
	@./deploy.sh stop

restart:
	@echo "Restarting services..."
	@./deploy.sh restart

logs:
	@echo "Showing logs..."
	@./deploy.sh logs

status:
	@echo "Checking status..."
	@./deploy.sh status

# Production commands
prod:
	@echo "Starting production environment..."
	@./deploy-prod.sh build start

# Maintenance commands
clean:
	@echo "Cleaning up..."
	@docker-compose down -v
	@docker system prune -f
	@docker volume prune -f

test:
	@echo "Testing API endpoints..."
	@echo "Health check:"
	@curl -s http://localhost:8182/health | jq .
	@echo ""
	@echo "API Info:"
	@curl -s http://localhost:8182/api/v1/openapi.json | jq '.info'

# Local development
local:
	@echo "Starting local development server..."
	@source venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload