# Docker Run Guide

This guide explains how to run the GuardianAI Fraud Prevention Chatbot using Docker and Docker Compose.

## Prerequisites

Before running the project with Docker, ensure you have the following installed:

1. **Docker** (version 19.03 or higher)
2. **Docker Compose** (version 1.27 or higher)

You can download Docker Desktop which includes both Docker and Docker Compose from [docker.com](https://www.docker.com/products/docker-desktop).

## Quick Start

To run the entire GuardianAI project with one command:

```bash
docker-compose up --build
```

This will:
1. Build all service images
2. Start all services (backend, database, frontend)
3. Create necessary network connections between services

## Accessing the Services

Once the containers are running, you can access the services at:

- **Backend API**: http://localhost:8000
- **Frontend Web App**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432 (PostgreSQL)

## Detailed Docker Commands

### 1. Build and Start All Services

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode (background)
docker-compose up --build -d
```

### 2. View Service Logs

```bash
# View logs for all services
docker-compose logs

# View logs for a specific service
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f
```

### 3. Stop Services

```bash
# Stop all services
docker-compose down

# Stop services and remove volumes (including database data)
docker-compose down -v
```

### 4. Rebuild Specific Services

```bash
# Rebuild only the backend service
docker-compose build backend

# Rebuild and restart a specific service
docker-compose up --build backend
```

### 5. Run Commands in Running Containers

```bash
# Run a shell in the backend container
docker-compose exec backend /bin/bash

# Run a Python command in the backend container
docker-compose exec backend python -c "print('Hello from backend container')"

# Run tests in the backend container
docker-compose exec backend python -m pytest
```

## Service Details

### Backend API Service

- **Image**: Built from `backend/Dockerfile`
- **Port**: 8000
- **Dependencies**: Database service
- **Technology**: Python, FastAPI
- **Key Features**:
  - RESTful API endpoints for fraud detection
  - Integration with all AI models
  - Database connectivity
  - Automatic reloading during development

### Database Service

- **Image**: postgres:13
- **Port**: 5432
- **Environment**:
  - User: user
  - Password: password
  - Database: guardianai
- **Persistence**: Data is stored in a Docker volume
- **Initialization**: Database schema is initialized from `init.sql`

### Frontend Web Service

- **Image**: Built from `frontend/web/Dockerfile`
- **Port**: 3000
- **Dependencies**: Backend API service
- **Technology**: React, Node.js
- **Key Features**:
  - Web-based chat interface
  - Real-time fraud analysis
  - Media upload capabilities

### Documentation Service

- **Image**: squidfunk/mkdocs-material
- **Port**: 8001
- **Technology**: MkDocs with Material theme
- **Features**:
  - Live documentation preview
  - Automatic rebuilding on file changes

## Environment Variables

The services use the following environment variables (configured in docker-compose.yml):

### Backend
- `DATABASE_URL`: Connection string for PostgreSQL database
- `SECRET_KEY`: Secret key for JWT token generation

### Frontend
- `REACT_APP_API_URL`: URL for backend API (set to http://backend:8000 for container communication)

## Data Persistence

The PostgreSQL database data is stored in a Docker volume named `postgres_data`. This ensures that data persists even when containers are stopped or removed.

To completely reset the database:
```bash
docker-compose down -v
docker-compose up --build
```

## Troubleshooting

### Common Issues and Solutions

1. **Port Already in Use**
   - Error: "port is already allocated"
   - Solution: Stop other services using the ports or modify port mappings in docker-compose.yml

2. **Permission Denied Errors**
   - Error: Permission denied when accessing files
   - Solution: Ensure Docker has proper file access permissions

3. **Database Connection Issues**
   - Error: Cannot connect to database
   - Solution: Check that the database service is running and environment variables are correct

4. **Frontend Cannot Reach Backend**
   - Error: Network errors in browser console
   - Solution: Verify the REACT_APP_API_URL environment variable and that both services are running

### Checking Service Status

```bash
# List running containers
docker-compose ps

# Check if a specific service is healthy
docker-compose ps backend
```

## Development Workflow

1. **Make Code Changes**
   - Modify files in your local directories
   - Changes are automatically reflected in containers due to volume mounting

2. **Test Changes**
   - Services with `--reload` flags automatically restart when code changes
   - Manual restart: `docker-compose restart <service>`

3. **Add New Dependencies**
   - Update requirements.txt or package.json
   - Rebuild the affected service: `docker-compose build <service>`

4. **Run Tests**
   - Execute tests in containers: `docker-compose exec <service> <test-command>`

## Production Considerations

For production deployment, consider the following changes:

1. **Security**:
   - Use strong passwords and secrets
   - Enable SSL/TLS
   - Configure proper firewall rules

2. **Performance**:
   - Use production-ready database settings
   - Configure appropriate resource limits
   - Implement load balancing

3. **Monitoring**:
   - Add health checks
   - Implement logging aggregation
   - Set up alerting

4. **Scaling**:
   - Use Docker Swarm or Kubernetes for orchestration
   - Implement horizontal scaling for stateless services

## Stopping and Cleanup

To stop all services:
```bash
docker-compose down
```

To stop services and remove all data (including database):
```bash
docker-compose down -v
```

To remove all Docker resources (images, containers, networks):
```bash
# Warning: This removes resources for all Docker projects
docker system prune -a
```

With this setup, you can easily run the complete GuardianAI Fraud Prevention Chatbot system with a single command, making development and deployment straightforward.