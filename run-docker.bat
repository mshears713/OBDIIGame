@echo off
REM Launch script for ECU Rogue using Docker on Windows
REM Compatible with Windows 10/11 with Docker Desktop

echo ==================================
echo    ECU Rogue - Docker Launcher
echo ==================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if Docker daemon is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker daemon is not running
    echo Please start Docker Desktop
    pause
    exit /b 1
)

echo Docker detected and running!
echo.

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo docker-compose not found, using docker commands...
    echo.
    echo Building image...
    docker build -t ecu-rogue .
    echo.
    echo Starting game...
    docker run -it --rm -v "%cd%/saves:/app/saves" ecu-rogue
) else (
    echo Using docker-compose...
    docker-compose up --build
)

pause
