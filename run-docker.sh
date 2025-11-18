#!/bin/bash
# Launch script for ECU Rogue using Docker
# Compatible with Linux, macOS, and WSL

set -e

echo "=================================="
echo "   ECU Rogue - Docker Launcher"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed or not in PATH"
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "ERROR: Docker daemon is not running"
    echo "Please start Docker Desktop or the Docker service"
    exit 1
fi

echo "Docker detected and running!"
echo ""

# Check if docker-compose is available
if command -v docker-compose &> /dev/null; then
    echo "Using docker-compose..."
    docker-compose up --build
else
    echo "docker-compose not found, using docker commands..."
    echo ""
    echo "Building image..."
    docker build -t ecu-rogue .
    echo ""
    echo "Starting game..."
    docker run -it --rm -v "${PWD}/saves:/app/saves" ecu-rogue
fi
