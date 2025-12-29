# Docker Setup Guide

This guide explains how to build and run the Atheist AI backend using Docker.

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose (usually included with Docker Desktop)

> **⚠️ Docker Not Found?** If you see `docker : The term 'docker' is not recognized`, see [DOCKER_SETUP.md](DOCKER_SETUP.md) for installation instructions.

## Quick Start

### 1. Build the Docker Image

**⚠️ Important:** Run this command from the **project root directory**, not from the `backend` folder.

From the project root:

```bash
# Make sure you're in the project root
cd C:\Users\Mohd Aftaab\atheist_rag

# Build the image
docker build -f backend/Dockerfile -t atheist-ai-backend .
```

### 2. Run with Docker Compose (Recommended)

Create a `.env` file in the project root (or use existing `backend/.env`):

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/database
OPENAI_API_KEY=your-openai-api-key
REDIS_URL=redis://localhost:6379  # Optional
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

Then run:

```bash
docker-compose up -d
```

The backend will be available at `http://localhost:8000`

### 3. Run with Docker (Manual)

```bash
docker run -d \
  --name atheist-ai-backend \
  -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URL=postgresql://user:password@host:port/database \
  -e OPENAI_API_KEY=your-openai-api-key \
  -e CORS_ORIGINS=http://localhost:3000 \
  atheist-ai-backend
```

## Environment Variables

Required environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Secret key for JWT tokens | `your-secret-key-here` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-proj-...` |

Optional environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_URL` | Redis connection string (for caching) | Empty (caching disabled) |
| `CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:3000` |

## Docker Commands

### Build the image
```bash
docker build -f backend/Dockerfile -t atheist-ai-backend .
```

### Run container
```bash
docker-compose up -d
# or
docker run -d -p 8000:8000 --env-file backend/.env atheist-ai-backend
```

### View logs
```bash
docker-compose logs -f backend
# or
docker logs -f atheist-ai-backend
```

### Stop container
```bash
docker-compose down
# or
docker stop atheist-ai-backend
```

### Remove container
```bash
docker-compose down -v
# or
docker rm -f atheist-ai-backend
```

### Rebuild after code changes
```bash
docker-compose up -d --build
```

### Execute commands in container
```bash
docker exec -it atheist-ai-backend bash
```

## Health Check

The container includes a health check that verifies the API is responding:

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' atheist-ai-backend

# Manual health check
curl http://localhost:8000/api/v1/health
```

## Production Deployment

### 1. Build for Production

```bash
docker build -f backend/Dockerfile -t atheist-ai-backend:latest .
```

### 2. Tag for Registry

```bash
docker tag atheist-ai-backend:latest your-registry/atheist-ai-backend:latest
```

### 3. Push to Registry

```bash
docker push your-registry/atheist-ai-backend:latest
```

### 4. Deploy

Deploy to your platform (Railway, Render, AWS ECS, etc.) using the Docker image.

## Troubleshooting

### Container won't start

1. Check logs:
   ```bash
   docker logs atheist-ai-backend
   ```

2. Verify environment variables:
   ```bash
   docker exec atheist-ai-backend env
   ```

3. Test database connection:
   ```bash
   docker exec -it atheist-ai-backend python -c "from backend.app.database import engine; engine.connect()"
   ```

### Port already in use

Change the port mapping in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Use port 8001 instead
```

### Permission issues

The Dockerfile creates a non-root user (`appuser`) for security. If you encounter permission issues, check file ownership.

### Large image size

The image includes FAISS and sentence-transformers which can be large. Consider:
- Using multi-stage builds
- Using `.dockerignore` to exclude unnecessary files
- Using Alpine-based images (may require additional dependencies)

## Development with Docker

For development, you can mount your code as a volume:

```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    volumes:
      - ./backend:/app/backend
      - ./quran_retrieval2.py:/app/quran_retrieval2.py
      - ./llm_explainer.py:/app/llm_explainer.py
    environment:
      - ENV=development
```

Run with:
```bash
docker-compose -f docker-compose.dev.yml up
```

## Security Notes

- Never commit `.env` files with secrets
- Use Docker secrets or environment variables for production
- The container runs as a non-root user for security
- Health checks help monitor container status
- Use HTTPS in production (configure reverse proxy)

## Next Steps

- Set up CI/CD pipeline to build and push Docker images
- Configure reverse proxy (nginx/traefik) for HTTPS
- Set up monitoring and logging
- Configure auto-scaling based on load

