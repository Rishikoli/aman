@echo off
REM AMAN Docker Helper Script for Windows
REM This script provides convenient commands for managing the AMAN Docker environment

setlocal enabledelayedexpansion

REM Function to check if Docker is running
:check_docker
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker and try again.
    exit /b 1
)
goto :eof

REM Function to start development environment
:start_dev
echo [INFO] Starting AMAN development environment...
call :check_docker
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
echo [INFO] Development environment started successfully!
echo [INFO] Frontend: http://localhost:3000
echo [INFO] Backend API: http://localhost:3001
echo [INFO] Superset: http://localhost:8088
echo [INFO] PostgreSQL: localhost:5432
echo [INFO] Redis: localhost:6379
goto :eof

REM Function to start production environment
:start_prod
echo [INFO] Starting AMAN production environment...
call :check_docker
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
echo [INFO] Production environment started successfully!
goto :eof

REM Function to stop all services
:stop
echo [INFO] Stopping AMAN services...
docker-compose down
echo [INFO] All services stopped.
goto :eof

REM Function to restart services
:restart
echo [INFO] Restarting AMAN services...
call :stop
timeout /t 2 /nobreak >nul
call :start_dev
goto :eof

REM Function to view logs
:logs
if "%~2"=="" (
    docker-compose logs -f
) else (
    docker-compose logs -f %2
)
goto :eof

REM Function to run database migrations
:migrate
echo [INFO] Running database migrations...
docker-compose exec backend npm run migrate
echo [INFO] Database migrations completed.
goto :eof

REM Function to seed database
:seed
echo [INFO] Seeding database with sample data...
docker-compose exec backend npm run seed
echo [INFO] Database seeding completed.
goto :eof

REM Function to clean up Docker resources
:cleanup
echo [WARNING] This will remove all AMAN containers, networks, and volumes.
set /p confirm="Are you sure? (y/N): "
if /i "%confirm%"=="y" (
    echo [INFO] Cleaning up Docker resources...
    docker-compose down -v --remove-orphans
    docker system prune -f
    echo [INFO] Cleanup completed.
) else (
    echo [INFO] Cleanup cancelled.
)
goto :eof

REM Function to show help
:show_help
echo AMAN Docker Helper Script for Windows
echo.
echo Usage: %0 [COMMAND]
echo.
echo Commands:
echo   dev       Start development environment
echo   prod      Start production environment
echo   stop      Stop all services
echo   restart   Restart all services
echo   logs      View logs (optionally specify service name)
echo   migrate   Run database migrations
echo   seed      Seed database with sample data
echo   cleanup   Remove all containers, networks, and volumes
echo   help      Show this help message
echo.
echo Examples:
echo   %0 dev                 # Start development environment
echo   %0 logs backend        # View backend service logs
echo   %0 cleanup             # Clean up all Docker resources
goto :eof

REM Main script logic
if "%1"=="dev" (
    call :start_dev
) else if "%1"=="prod" (
    call :start_prod
) else if "%1"=="stop" (
    call :stop
) else if "%1"=="restart" (
    call :restart
) else if "%1"=="logs" (
    call :logs %*
) else if "%1"=="migrate" (
    call :migrate
) else if "%1"=="seed" (
    call :seed
) else if "%1"=="cleanup" (
    call :cleanup
) else if "%1"=="help" (
    call :show_help
) else if "%1"=="--help" (
    call :show_help
) else if "%1"=="-h" (
    call :show_help
) else if "%1"=="" (
    echo [ERROR] No command specified.
    call :show_help
    exit /b 1
) else (
    echo [ERROR] Unknown command: %1
    call :show_help
    exit /b 1
)