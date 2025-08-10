# KortekStream API - Deployment Guide

## Quick Start

### Development Deployment
```bash
# Clone and setup
git clone <repository-url>
cd fastapi_app

# Deploy with development settings
./deploy.sh build start

# Access the API
curl http://localhost:8182/health
```

### Production Deployment
```bash
# Setup production environment
cp .env.production .env
# Edit .env with your production settings

# Deploy with production settings
./deploy-prod.sh build start
```

## Available Endpoints

- **Health Check**: `GET http://localhost:8182/health`
- **API Documentation**: `GET http://localhost:8182/docs`
- **Home**: `GET http://localhost:8182/api/v1/home`
- **Latest Anime**: `GET http://localhost:8182/api/v1/anime-terbaru`
- **Release Schedule**: `GET http://localhost:8182/api/v1/jadwal-rilis`
- **Search**: `GET http://localhost:8182/api/v1/search?q=naruto`

## Service Status

Current deployment is running on:
- **API Port**: 8182
- **Redis Port**: 6379
- **Environment**: Development
- **CORS**: Enabled for all origins (*)

## Management Commands

```bash
# Development
./deploy.sh start|stop|restart|build|logs|status

# Production
./deploy-prod.sh start|stop|restart|build|logs|status
```

## Configuration

Key environment variables:
- `PORT=8182` - API external port
- `DOMAIN=localhost` - Server domain
- `PROTOCOL=http` - Server protocol
- `BACKEND_CORS_ORIGINS=*` - CORS settings

## Docker Services

1. **kortekstream-api**: FastAPI application
2. **kortekstream-redis**: Redis cache server

Both services include health checks and automatic restart policies.