# Dockerfile for ECU Rogue - Modular Python Roguelike
# Compatible with Windows, WSL, Linux, and macOS

# Use official Python runtime as base image
FROM python:3.11-slim

# Set metadata labels
LABEL maintainer="Game Development Team"
LABEL description="ECU Rogue - A modular Python roguelike exploring automotive ECU systems"
LABEL version="1.0.0"

# Set working directory in container
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies (if needed in future)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Install the package in editable mode
RUN pip install -e .

# Create a volume mount point for save games
VOLUME ["/app/saves"]

# Set the default command to run the game
CMD ["python", "main.py"]

# Alternative: Use the installed console script
# CMD ["ecu-rogue"]
