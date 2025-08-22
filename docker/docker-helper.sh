#!/bin/bash

# AMAN Docker Helper Script
# This script provides convenient commands for managing the AMAN Docker environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
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
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to start development environment
start_dev() {
    print_status "Starting AMAN development environment..."
    check_docker
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
    print_status "Development environment started successfully!"
    print_status "Frontend: http://localhost:3000"
    print_status "Backend API: http://localhost:3001"
    print_status "Superset: http://localhost:8088"
    print_status "PostgreSQL: localhost:5432"
    print_status "Redis: localhost:6379"
}

# Function to start production environment
start_prod() {
    print_status "Starting AMAN production environment..."
    check_docker
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
    print_status "Production environment started successfully!"
}

# Function to stop all services
stop() {
    print_status "Stopping AMAN services..."
    docker-compose down
    print_status "All services stopped."
}

# Function to restart services
restart() {
    print_status "Restarting AMAN services..."
    stop
    sleep 2
    start_dev
}

# Function to view logs
logs() {
    if [ -z "$1" ]; then
        docker-compose logs -f
    else
        docker-compose logs -f "$1"
    fi
}

# Function to run database migrations
migrate() {
    print_status "Running database migrations..."
    docker-compose exec backend npm run migrate
    print_status "Database migrations completed."
}

# Function to seed database
seed() {
    print_status "Seeding database with sample data..."
    docker-compose exec backend npm run seed
    print_status "Database seeding completed."
}

# Function to clean up Docker resources
cleanup() {
    print_warning "This will remove all AMAN containers, networks, and volumes."
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Cleaning up Docker resources..."
        docker-compose down -v --remove-orphans
        docker system prune -f
        print_status "Cleanup completed."
    else
        print_status "Cleanup cancelled."
    fi
}

# Function to show help
show_help() {
    echo "AMAN Docker Helper Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  dev       Start development environment"
    echo "  prod      Start production environment"
    echo "  stop      Stop all services"
    echo "  restart   Restart all services"
    echo "  logs      View logs (optionally specify service name)"
    echo "  migrate   Run database migrations"
    echo "  seed      Seed database with sample data"
    echo "  cleanup   Remove all containers, networks, and volumes"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 dev                 # Start development environment"
    echo "  $0 logs backend        # View backend service logs"
    echo "  $0 cleanup             # Clean up all Docker resources"
}

# Main script logic
case "$1" in
    "dev")
        start_dev
        ;;
    "prod")
        start_prod
        ;;
    "stop")
        stop
        ;;
    "restart")
        restart
        ;;
    "logs")
        logs "$2"
        ;;
    "migrate")
        migrate
        ;;
    "seed")
        seed
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    "")
        print_error "No command specified."
        show_help
        exit 1
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac