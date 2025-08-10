# KortekStream API

FastAPI-based anime streaming API with dynamic configuration and Docker deployment.

## Features

- 🚀 FastAPI with automatic OpenAPI documentation
- 🐳 Docker containerization with Docker Compose
- 📊 Redis caching for improved performance
- 🔧 Dynamic configuration based on environment
- 🌐 CORS support for cross-origin requests
- 📝 Comprehensive logging
- 🏥 Health check endpoints
- 📖 Interactive Swagger UI documentation

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git (for cloning the repository)

### Deployment

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd fastapi_app
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

3. **Deploy using the deployment script:**
   ```bash
   # Make the script executable
   chmod +x deploy.sh
   
   # Build and start the application
   ./deploy.sh build start
   ```

4. **Access the application:**
   - API Base URL: http://localhost:8182
   - Swagger UI: http://localhost:8182/docs
   - Health Check: http://localhost:8182/health

### Manual Deployment

If you prefer manual deployment:

```bash
# Build the images
docker-compose build

# Start the services
unset PORT  # Important: unset PORT env var to avoid conflicts
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Configuration

### Environment Variables

The application uses the following environment variables (defined in `.env`):

#### API Configuration
- `API_V1_STR`: API version prefix (default: `/api/v1`)
- `PROJECT_NAME`: Project name for documentation (default: `"KortekStream API"`)

#### Server Configuration
- `DOMAIN`: Server domain (default: `localhost`)
- `PROTOCOL`: Server protocol (default: `http`)
- `PORT`: External port mapping (default: `8182`)
- `WORKERS`: Number of worker processes (default: `1`)

#### CORS Configuration
- `BACKEND_CORS_ORIGINS`: Allowed CORS origins (default: `*`)

#### Anime Source Configuration
- `SAMEHADAKU_BASE_URL`: Base URL for Samehadaku source
- `SAMEHADAKU_SEARCH_URL`: Search URL for Samehadaku
- `SAMEHADAKU_API_URL`: API URL for Samehadaku

#### Cache Configuration
- `CACHE_TTL`: Default cache TTL in seconds (default: `600`)
- `CACHE_LONG_TTL`: Long cache TTL in seconds (default: `3600`)
- `CACHE_VERY_LONG_TTL`: Very long cache TTL in seconds (default: `86400`)

#### Redis Configuration
- `REDIS_HOST`: Redis host (default: `redis`)
- `REDIS_PORT`: Redis port (default: `6379`)
- `REDIS_DB`: Redis database number (default: `0`)

### Dynamic Configuration

The application automatically adjusts its configuration based on the environment:

- **Server URL**: Automatically generated based on `DOMAIN`, `PROTOCOL`, and `PORT`
- **CORS Origins**: Supports wildcard (`*`) or comma-separated list of origins
- **Swagger UI**: Uses dynamic server URL (not hardcoded)

## Deployment Script Usage

The `deploy.sh` script provides convenient commands for managing the application:

```bash
# Start the application
./deploy.sh start

# Stop the application
./deploy.sh stop

# Restart the application
./deploy.sh restart

# Build Docker images
./deploy.sh build

# Build and start
./deploy.sh build start

# Show logs
./deploy.sh logs

# Show service status
./deploy.sh status

# Show help
./deploy.sh help
```

## API Endpoints

### Health Check
- `GET /health` - Application health status

### Home
- `GET /api/v1/home` - Home page data

### Anime
- `GET /api/v1/anime-terbaru` - Latest anime releases
- `GET /api/v1/jadwal-rilis` - Release schedule
- `GET /api/v1/anime/{anime_id}` - Anime details
- `GET /api/v1/episode/{episode_id}` - Episode details

### Search
- `GET /api/v1/search` - Search anime

### Movies
- `GET /api/v1/movie` - Movie listings

## Development

### Local Development

1. **Set up Python environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run locally:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Docker Development

```bash
# Build development image
docker build -t fastapi_app-dev .

# Run development container
docker run -p 8000:8001 -v $(pwd):/app fastapi_app-dev
```

## Production Deployment

For production deployment:

1. **Update configuration:**
   ```bash
   cp .env.production .env
   # Edit .env with your production settings
   ```

2. **Set production domain:**
   ```bash
   # In .env file
   DOMAIN=yourdomain.com
   PROTOCOL=https
   PORT=443
   ```

3. **Deploy:**
   ```bash
   ./deploy.sh build start
   ```

## Monitoring and Logs

### View Logs
```bash
# All services
./deploy.sh logs

# Specific service
docker-compose logs -f api
docker-compose logs -f redis
```

### Health Monitoring
```bash
# Check service status
./deploy.sh status

# Manual health check
curl http://localhost:8182/health
```

## Troubleshooting

### Common Issues

1. **Port conflicts:**
   - Make sure no other services are using port 8182
   - Unset the `PORT` environment variable: `unset PORT`

2. **Docker permission issues:**
   - Make sure your user is in the docker group
   - Try running with `sudo` if necessary

3. **Service not starting:**
   - Check logs: `./deploy.sh logs`
   - Verify configuration in `.env` file
   - Ensure Docker is running

4. **API not responding:**
   - Wait for services to be fully ready (10-15 seconds)
   - Check container health: `docker-compose ps`
   - Verify port mapping: `docker port kortekstream-api`

### Reset Everything

If you need to completely reset the deployment:

```bash
# Stop and remove everything
docker-compose down -v
docker system prune -f

# Rebuild and start fresh
./deploy.sh build start
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.