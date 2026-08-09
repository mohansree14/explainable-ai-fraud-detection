# Docker Troubleshooting Guide

This guide helps you resolve common issues when running the GuardianAI project with Docker.

## Common Issues and Solutions

### 1. Docker Daemon Not Running

**Error Message**: 
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```
or
```
error during connect: Head "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping": open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

**Solution**:
1. Make sure Docker Desktop is running
   - Look for the Docker icon in your system tray (Windows) or menu bar (Mac)
   - If not running, start Docker Desktop from your applications menu
2. Wait for Docker Desktop to finish starting (it may take a minute)
3. Try the command again

### 2. Permission Denied

**Error Message**:
```
permission denied while trying to connect to the Docker daemon socket
```

**Solution** (Linux):
1. Add your user to the docker group:
   ```bash
   sudo usermod -aG docker $USER
   ```
2. Log out and log back in for the changes to take effect

**Solution** (Windows):
1. Make sure you're running the command prompt or terminal as Administrator
2. Or ensure your user account has permission to use Docker

### 3. Port Already in Use

**Error Message**:
```
Bind for 0.0.0.0:8000 failed: port is already allocated
```

**Solution**:
1. Find what's using the port:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   
   # Mac/Linux
   lsof -i :8000
   ```
2. Stop the process using the port, or change the port mapping in docker-compose.yml

### 4. File Sharing Issues (Windows/Mac)

**Error Message**:
```
ERROR: for backend  Cannot create container for service backend: b'Drive has not been shared'
```

**Solution**:
1. Open Docker Desktop Settings
2. Go to "Resources" → "File Sharing"
3. Add the directory where your project is located
4. Apply and restart Docker Desktop

### 5. Insufficient Resources

**Error Message**:
```
failed to solve: rpc error: code = Unknown desc = failed to solve with frontend dockerfile.v0
```

**Solution**:
1. Increase Docker's resources:
   - Open Docker Desktop Settings
   - Go to "Resources" → "Advanced"
   - Increase Memory and CPU allocation
   - Apply and restart Docker Desktop

### 6. Network Issues

**Error Message**:
```
Could not resolve host: registry-1.docker.io
```

**Solution**:
1. Check your internet connection
2. If behind a corporate firewall, configure Docker Desktop to use your proxy settings
3. Try using a different DNS server (e.g., Google's 8.8.8.8)

## Windows-Specific Issues

### Docker Desktop Won't Start

1. Make sure virtualization is enabled in BIOS/UEFI
2. Ensure Windows Subsystem for Linux (WSL) is installed and up to date
3. Try reinstalling Docker Desktop

### Line Ending Issues

If you see errors related to `\r` characters:

1. Configure Git to handle line endings properly:
   ```bash
   git config --global core.autocrlf false
   ```

2. Or convert line endings in your files:
   ```bash
   dos2unix docker-compose.yml
   ```

## Mac-Specific Issues

### Docker Desktop Requires Newer macOS

Update to the latest version of macOS that your hardware supports.

### M1/M2 Chip Compatibility

Some images may not work on Apple Silicon. Look for ARM64 compatible images or build from source.

## Linux-Specific Issues

### Docker Service Not Started

Start the Docker service:
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### User Permissions

Add your user to the docker group:
```bash
sudo groupadd docker
sudo usermod -aG docker $USER
```

Then log out and back in.

## Testing Docker Installation

To verify Docker is working correctly:

```bash
# Test Docker
docker run hello-world

# Test Docker Compose
docker-compose version
```

## GuardianAI Specific Troubleshooting

### Backend Service Fails to Start

1. Check that all required files are present:
   - backend/Dockerfile
   - requirements.txt
   - backend/app/main.py

2. Verify the backend service logs:
   ```bash
   docker-compose logs backend
   ```

### Frontend Service Issues

1. Ensure the frontend Dockerfile exists:
   - frontend/web/Dockerfile

2. Check that package.json is present in frontend/web/

3. Verify the frontend service logs:
   ```bash
   docker-compose logs frontend-web
   ```

### Database Connection Issues

1. Verify database credentials in docker-compose.yml match your configuration
2. Check that the database service is running:
   ```bash
   docker-compose ps
   ```
3. Test database connectivity:
   ```bash
   docker-compose exec db pg_isready
   ```

### Model Integration Issues

If you're having issues with model integration:

1. Verify that all model files are present in the models/ directory
2. Check that the Python path is correctly configured in the routers
3. Ensure all model dependencies are listed in requirements.txt

## Advanced Troubleshooting

### Clean Slate Approach

If nothing else works, try resetting Docker:

```bash
# Stop all containers
docker-compose down

# Remove all containers, networks, and volumes
docker-compose down -v --remove-orphans

# Remove unused Docker objects
docker system prune -a

# Rebuild and start
docker-compose up --build
```

### Debugging Inside Containers

Access a running container for debugging:

```bash
# Access backend container
docker-compose exec backend /bin/bash

# Access database container
docker-compose exec db psql -U user -d guardianai
```

### Checking Resource Usage

Monitor container resource usage:

```bash
# View resource usage
docker stats

# Check container details
docker-compose ps
```

## Getting Help

If you're still having issues:

1. Check the Docker documentation: https://docs.docker.com/
2. Look at Docker Desktop troubleshooting: https://docs.docker.com/desktop/troubleshoot/overview/
3. Search for your specific error message on Stack Overflow
4. Check the Docker community forums

For GuardianAI-specific issues, refer to:
- [DOCKER_RUN_GUIDE.md](DOCKER_RUN_GUIDE.md)
- [README.md](README.md)
- Project documentation in the [docs/](docs/) directory

Remember to always check that Docker Desktop is running before attempting to use Docker commands.