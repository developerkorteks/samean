# Docker Deployment Guide

This guide explains how to deploy the KortekStream API using Docker with flexible domain configuration.

## 🚀 Quick Start

### 1. Environment Setup

Copy the environment template:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```bash
# For local development
DOMAIN=localhost
PROTOCOL=http
PORT=8001

# For production
DOMAIN=yourdomain.com
PROTOCOL=https
PORT=443
```

### 2. Deploy

Use the deployment script:
```bash
# Development mode
./deploy.sh development

# Production mode (with Nginx)
./deploy.sh production

# API only (no Nginx)
./deploy.sh api-only
```

## 📋 Deployment Modes

### Development Mode
- API service on port 8001
- Redis for caching
- Hot reload enabled
- Debug logging

```bash
./deploy.sh development
```

### Production Mode
- API service behind Nginx reverse proxy
- SSL/TLS support (configure certificates)
- Rate limiting
- Gzip compression
- Security headers

```bash
./deploy.sh production
```

### API Only Mode
- Just API and Redis services
- No reverse proxy
- Useful for custom setups

```bash
./deploy.sh api-only
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `DOMAIN` | Your domain name | `localhost` | `api.yourdomain.com` |
| `PROTOCOL` | HTTP protocol | `http` | `https` |
| `PORT` | API port | `8001` | `443` |
| `WORKERS` | Uvicorn workers | `1` | `4` |
| `BACKEND_CORS_ORIGINS` | CORS origins | `*` | `https://yourdomain.com` |

### Swagger UI Configuration

The Swagger UI automatically adapts to your domain configuration:

- **Local**: `http://localhost:8001/docs`
- **Production**: `https://yourdomain.com/docs`
- **Custom domain**: `https://api.yourdomain.com/docs`

The OpenAPI schema dynamically detects:
- Request protocol (HTTP/HTTPS)
- Host headers
- Forwarded headers (for reverse proxies)
- Environment configuration

## 🌐 Domain Configuration Examples

### Local Development
```env
DOMAIN=localhost
PROTOCOL=http
PORT=8001
BACKEND_CORS_ORIGINS=*
```

### Production with Custom Domain
```env
DOMAIN=api.yourdomain.com
PROTOCOL=https
PORT=443
BACKEND_CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Subdomain Setup
```env
DOMAIN=scrapeapi.yourdomain.com
PROTOCOL=https
PORT=443
BACKEND_CORS_ORIGINS=https://yourdomain.com
```

## 🔒 SSL/HTTPS Setup

### 1. Obtain SSL Certificates

Using Let's Encrypt:
```bash
# Install certbot
sudo apt install certbot

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com
```

### 2. Configure SSL in Docker

Create SSL directory:
```bash
mkdir ssl
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem
```

### 3. Update Nginx Configuration

Uncomment HTTPS server block in `nginx.conf` and update domain name.

## 📊 Monitoring and Logs

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f nginx
docker-compose logs -f redis
```

### Health Checks
```bash
# API health
curl http://localhost:8001/health

# Through Nginx
curl http://localhost/health
```

### Container Status
```bash
docker-compose ps
```

## 🔄 Updates and Maintenance

### Update Application
```bash
# Pull latest changes
git pull

# Rebuild and restart
./deploy.sh production
```

### Backup Redis Data
```bash
docker-compose exec redis redis-cli BGSAVE
docker cp kortekstream-redis:/data/dump.rdb ./backup/
```

### Scale Services
```bash
# Scale API instances
docker-compose up -d --scale api=3
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   sudo lsof -i :8001
   
   # Change port in .env
   PORT=8002
   ```

2. **Permission denied**
   ```bash
   # Fix permissions
   sudo chown -R $USER:$USER .
   chmod +x deploy.sh
   ```

3. **SSL certificate issues**
   ```bash
   # Check certificate validity
   openssl x509 -in ssl/cert.pem -text -noout
   ```

4. **CORS errors**
   ```bash
   # Update CORS origins in .env
   BACKEND_CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   ```

### Debug Mode

Enable debug logging:
```bash
# Add to .env
DEBUG=true

# Restart services
docker-compose restart api
```

## 📈 Performance Tuning

### Production Optimizations

1. **Increase workers**
   ```env
   WORKERS=4  # CPU cores * 2
   ```

2. **Redis memory optimization**
   ```bash
   # In docker-compose.yml, Redis command already optimized:
   # --maxmemory 256mb --maxmemory-policy allkeys-lru
   ```

3. **Nginx caching**
   ```nginx
   # Add to nginx.conf
   proxy_cache_path /tmp/nginx_cache levels=1:2 keys_zone=api_cache:10m max_size=100m;
   proxy_cache api_cache;
   proxy_cache_valid 200 5m;
   ```

## 🔐 Security Considerations

### Production Security Checklist

- [ ] Use HTTPS with valid SSL certificates
- [ ] Restrict CORS origins
- [ ] Enable rate limiting (configured in Nginx)
- [ ] Use non-root user in containers (already configured)
- [ ] Keep dependencies updated
- [ ] Monitor logs for suspicious activity
- [ ] Use secrets management for sensitive data

### Environment Security
```env
# Don't use wildcards in production
BACKEND_CORS_ORIGINS=https://yourdomain.com

# Use specific Redis configuration
REDIS_PASSWORD=your_secure_password
```

## 📞 Support

For issues and questions:
1. Check logs: `docker-compose logs -f`
2. Verify configuration: `cat .env`
3. Test health endpoint: `curl http://localhost:8001/health`
4. Review this documentation

## 🎯 Next Steps

After successful deployment:
1. Set up monitoring (Prometheus/Grafana)
2. Configure log aggregation (ELK stack)
3. Set up automated backups
4. Implement CI/CD pipeline
5. Configure load balancing for high availability