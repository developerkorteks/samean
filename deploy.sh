#!/bin/bash

# KortekStream API Deployment Script
# Usage: ./deploy.sh [start|stop|restart|logs|status|build]

set -e

PROJECT_NAME="KortekStream API"
COMPOSE_FILE="docker-compose.yml"

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

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to check if docker-compose is available
check_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "docker-compose is not installed or not in PATH."
        exit 1
    fi
}

# Function to build the application
build_app() {
    print_status "Building $PROJECT_NAME..."
    docker-compose build --no-cache
    print_success "Build completed successfully!"
}

# Function to start the application
start_app() {
    print_status "Starting $PROJECT_NAME..."
    
    # Unset PORT environment variable if it exists to avoid conflicts
    unset PORT 2>/dev/null || true
    
    docker-compose up -d
    
    # Wait for services to be healthy
    print_status "Waiting for services to be ready..."
    sleep 10
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_success "$PROJECT_NAME started successfully!"
        print_status "API is available at: http://localhost:8182"
        print_status "Swagger UI is available at: http://localhost:8182/docs"
        print_status "Health check: http://localhost:8182/health"
    else
        print_error "Failed to start services. Check logs with: ./deploy.sh logs"
        exit 1
    fi
}

# Function to stop the application
stop_app() {
    print_status "Stopping $PROJECT_NAME..."
    docker-compose down
    print_success "$PROJECT_NAME stopped successfully!"
}

# Function to restart the application
restart_app() {
    print_status "Restarting $PROJECT_NAME..."
    stop_app
    start_app
}

# Function to show logs
show_logs() {
    print_status "Showing logs for $PROJECT_NAME..."
    docker-compose logs -f
}

# Function to show status
show_status() {
    print_status "Status of $PROJECT_NAME services:"
    docker-compose ps
    
    echo ""
    print_status "Testing API health..."
    if curl -s http://localhost:8182/health > /dev/null 2>&1; then
        print_success "API is healthy and responding!"
    else
        print_warning "API is not responding. Check logs with: ./deploy.sh logs"
    fi
}

# Function to show help
show_help() {
    echo "KortekStream API Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     Start the application"
    echo "  stop      Stop the application"
    echo "  restart   Restart the application"
    echo "  build     Build the Docker images"
    echo "  logs      Show application logs"
    echo "  status    Show service status"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start          # Start the application"
    echo "  $0 build start    # Build and start the application"
    echo "  $0 logs           # Show logs"
}

# Main script logic
main() {
    # Check prerequisites
    check_docker
    check_compose
    
    # Handle commands
    case "${1:-help}" in
        "start")
            start_app
            ;;
        "stop")
            stop_app
            ;;
        "restart")
            restart_app
            ;;
        "build")
            build_app
            if [ "$2" = "start" ]; then
                start_app
            fi
            ;;
        "logs")
            show_logs
            ;;
        "status")
            show_status
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@"