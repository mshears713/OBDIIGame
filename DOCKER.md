# Docker Guide for ECU Rogue

Complete guide for running ECU Rogue in Docker on Windows, WSL, Linux, and macOS.

## Quick Start

### Using Helper Scripts (Easiest)

**Linux/macOS/WSL:**
```bash
./run-docker.sh
```

**Windows (CMD or PowerShell):**
```cmd
run-docker.bat
```

### Using Docker Compose

```bash
docker-compose up --build
```

### Using Docker CLI

```bash
docker build -t ecu-rogue .
docker run -it --rm -v ${PWD}/saves:/app/saves ecu-rogue
```

---

## Installation by Platform

### Windows 10/11

#### Step 1: Install Docker Desktop

1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Run the installer
3. Enable WSL2 integration (recommended) during installation
4. Restart your computer when prompted

#### Step 2: Verify Installation

Open PowerShell or CMD and run:
```powershell
docker --version
docker-compose --version
```

#### Step 3: Run the Game

**Option A: Using the batch script**
```cmd
run-docker.bat
```

**Option B: Using Docker Compose**
```cmd
docker-compose up --build
```

**Option C: Using Docker CLI**

PowerShell:
```powershell
docker run -it --rm -v ${PWD}/saves:/app/saves ecu-rogue
```

CMD:
```cmd
docker run -it --rm -v %cd%/saves:/app/saves ecu-rogue
```

### Windows Subsystem for Linux (WSL2)

#### Step 1: Enable WSL2

```powershell
# In PowerShell as Administrator
wsl --install
wsl --set-default-version 2
```

#### Step 2: Install a Linux Distribution

Install Ubuntu from Microsoft Store or:
```powershell
wsl --install -d Ubuntu
```

#### Step 3: Install Docker Desktop (Recommended)

1. Install Docker Desktop for Windows
2. In Docker Desktop settings, enable WSL2 integration
3. Select your WSL2 distributions to integrate with

#### Step 4: Run in WSL

```bash
# In WSL terminal
cd ~
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame
./run-docker.sh
```

**Alternative: Install Docker directly in WSL**

```bash
# Update packages
sudo apt-get update

# Install Docker
sudo apt-get install -y docker.io docker-compose

# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and back in, then:
docker --version

# Run the game
./run-docker.sh
```

### Linux (Ubuntu/Debian)

#### Step 1: Install Docker

```bash
# Update package index
sudo apt-get update

# Install dependencies
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER
```

#### Step 2: Log out and back in

```bash
# Verify installation
docker --version
docker compose version
```

#### Step 3: Run the Game

```bash
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame
./run-docker.sh
```

### macOS

#### Step 1: Install Docker Desktop

1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. Drag Docker.app to Applications folder
3. Open Docker Desktop and follow setup wizard

#### Step 2: Verify Installation

```bash
docker --version
docker-compose --version
```

#### Step 3: Run the Game

```bash
git clone https://github.com/yourusername/OBDIIGame.git
cd OBDIIGame
./run-docker.sh
```

---

## Docker Commands Reference

### Building the Image

**First time build:**
```bash
docker build -t ecu-rogue .
```

**Rebuild from scratch (no cache):**
```bash
docker build --no-cache -t ecu-rogue .
```

**Using Docker Compose:**
```bash
docker-compose build
docker-compose build --no-cache  # Force rebuild
```

### Running the Container

**Basic run (interactive):**
```bash
docker run -it --rm ecu-rogue
```

**With save game persistence:**
```bash
docker run -it --rm -v ${PWD}/saves:/app/saves ecu-rogue
```

**Using Docker Compose:**
```bash
docker-compose up          # Run in foreground
docker-compose up -d       # Run in background (detached)
docker-compose up --build  # Build and run
```

### Managing Containers

**List running containers:**
```bash
docker ps
```

**List all containers (including stopped):**
```bash
docker ps -a
```

**Stop a running container:**
```bash
docker stop <container-id>
docker-compose down
```

**Remove stopped containers:**
```bash
docker container prune
```

### Managing Images

**List images:**
```bash
docker images
```

**Remove an image:**
```bash
docker rmi ecu-rogue
```

**Remove unused images:**
```bash
docker image prune
```

### Viewing Logs

**Docker run logs:**
```bash
docker logs <container-id>
```

**Docker Compose logs:**
```bash
docker-compose logs
docker-compose logs -f  # Follow logs
```

---

## Volume Management (Save Games)

### Where Save Games Are Stored

Save games are stored in the `saves/` directory in your project folder, which is mounted into the container.

**Project structure:**
```
OBDIIGame/
├── saves/              # Your save games here
│   ├── README.md
│   └── savegame.json  # Created when you save
├── Dockerfile
├── docker-compose.yml
└── ...
```

### Backing Up Save Games

```bash
# Create a backup
cp saves/savegame.json saves/savegame.backup.json

# Restore from backup
cp saves/savegame.backup.json saves/savegame.json

# Archive all saves
tar -czf saves-backup.tar.gz saves/
```

### Using Named Volumes (Alternative)

Edit `docker-compose.yml` to use named volumes instead of bind mounts:

```yaml
volumes:
  - game-saves:/app/saves

volumes:
  game-saves:
    driver: local
```

**Advantages:**
- Better performance on Windows/macOS
- Docker manages the volume

**Disadvantages:**
- Not directly accessible from host filesystem
- Need to use `docker cp` to extract saves

---

## Troubleshooting

### Docker is not running

**Error:** `Cannot connect to the Docker daemon`

**Solution:**
- **Windows/macOS:** Start Docker Desktop
- **Linux:** `sudo systemctl start docker`

### Permission denied

**Error:** `permission denied while trying to connect to Docker`

**Solution:**
```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and back in
```

### Port already in use

**Error:** `port is already allocated`

**Solution:**
```bash
# Stop other containers
docker-compose down
docker stop $(docker ps -q)
```

### Cannot find save games

**Issue:** Save games don't persist between runs

**Solution:**
Make sure you're using the volume mount flag:
```bash
docker run -it --rm -v ${PWD}/saves:/app/saves ecu-rogue
```

Or using Docker Compose (which includes the mount).

### Terminal display issues

**Issue:** Colors or characters not displaying correctly

**Solution:**
```bash
# Set TERM environment variable
docker run -it --rm -e TERM=xterm-256color -v ${PWD}/saves:/app/saves ecu-rogue
```

Or in `docker-compose.yml`:
```yaml
environment:
  - TERM=xterm-256color
```

### Build fails

**Error:** Various build errors

**Solution:**
```bash
# Clean up and rebuild
docker-compose down
docker system prune -a
docker-compose build --no-cache
```

### Game runs slow

**Issue:** Performance issues in Docker

**Solution:**
1. Allocate more resources to Docker in settings
2. On Windows/Mac, ensure WSL2 backend is enabled
3. Close other resource-intensive applications

---

## Advanced Usage

### Custom Python Version

Edit `Dockerfile` to use a different Python version:

```dockerfile
FROM python:3.9-slim    # or 3.10-slim, 3.11-slim, 3.12-slim
```

### Development Mode

Run with source code mounted for live editing:

```bash
docker run -it --rm \
  -v ${PWD}:/app \
  -v ${PWD}/saves:/app/saves \
  ecu-rogue
```

Or add to `docker-compose.yml`:

```yaml
volumes:
  - .:/app
  - ./saves:/app/saves
```

### Resource Limits

Add resource limits to `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
    reservations:
      cpus: '0.5'
      memory: 256M
```

### Multi-stage Builds

For smaller images, create a multi-stage build (advanced):

```dockerfile
# Builder stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "main.py"]
```

---

## Continuous Integration (CI)

### GitHub Actions Example

Create `.github/workflows/docker.yml`:

```yaml
name: Docker Build Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: docker build -t ecu-rogue .

      - name: Test container starts
        run: docker run --rm ecu-rogue python -c "import sys; sys.exit(0)"
```

---

## Security Best Practices

1. **Don't run as root (future improvement):**
   ```dockerfile
   RUN useradd -m appuser
   USER appuser
   ```

2. **Scan for vulnerabilities:**
   ```bash
   docker scan ecu-rogue
   ```

3. **Use specific Python versions:**
   ```dockerfile
   FROM python:3.11.5-slim  # Instead of python:3.11-slim
   ```

4. **Keep images updated:**
   ```bash
   docker-compose pull
   docker-compose build --no-cache
   ```

---

## Uninstalling

### Remove Images and Containers

```bash
# Stop and remove containers
docker-compose down

# Remove the image
docker rmi ecu-rogue

# Remove all unused Docker resources
docker system prune -a
```

### Uninstall Docker

**Windows/macOS:** Uninstall Docker Desktop from Control Panel/Applications

**Linux:**
```bash
sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```

---

## Additional Resources

- [Official Docker Documentation](https://docs.docker.com/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/install/)
- [Docker on WSL2](https://docs.docker.com/desktop/wsl/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices for Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

## Getting Help

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review Docker logs: `docker logs <container-id>`
3. Check Docker status: `docker info`
4. Visit Docker documentation
5. Open an issue on GitHub

---

**Happy Gaming!**
