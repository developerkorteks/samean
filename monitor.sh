#!/bin/bash

# KortekStream API Monitoring Script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Load environment variables if .env exists
if [ -f .env ]; then
    source .env
fi

PORT=${PORT:-8001}

echo "🔍 KortekStream API Monitoring Dashboard"
echo "========================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running!"
    exit 1
fi

# Check container status
print_status "Container Status:"
docker-compose ps

echo ""

# Check API health
print_status "API Health Check:"
if curl -f -s http://localhost:$PORT/health > /dev/null 2>&1; then
    print_success "API is healthy ✅"
    
    # Get API info
    API_INFO=$(curl -s http://localhost:$PORT/health)
    echo "  Response: $API_INFO"
else
    print_error "API is not responding ❌"
fi

echo ""

# Check Redis
print_status "Redis Status:"
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    print_success "Redis is running ✅"
    
    # Get Redis info
    REDIS_INFO=$(docker-compose exec -T redis redis-cli info memory | grep used_memory_human)
    echo "  Memory usage: $REDIS_INFO"
else
    print_error "Redis is not responding ❌"
fi

echo ""

# Check Nginx (if running)
if docker-compose ps nginx | grep -q "Up"; then
    print_status "Nginx Status:"
    if curl -f -s http://localhost/health > /dev/null 2>&1; then
        print_success "Nginx is running ✅"
    else
        print_warning "Nginx is running but not responding properly ⚠️"
    fi
    echo ""
fi

# Resource usage
print_status "Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" $(docker-compose ps -q)

echo ""

# Recent logs (last 10 lines)
print_status "Recent API Logs:"
docker-compose logs --tail=10 api

echo ""
echo "🔧 Quick Actions:"
echo "  View full logs: docker-compose logs -f"
echo "  Restart API: docker-compose restart api"
echo "  Stop all: docker-compose down"
echo "  Update: ./deploy.sh production"