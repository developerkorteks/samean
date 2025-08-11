import os
from typing import Dict, List, Optional, Union, Any
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "KortekStream API"
    
    # Server Configuration
    DOMAIN: str = "localhost"
    PROTOCOL: str = "http"
    PORT: int = 8001
    WORKERS: int = 1
    
    # Dynamic server URL based on environment
    @property
    def SERVER_URL(self) -> str:
        """Generate server URL based on domain and protocol"""
        if self.PORT in [80, 443]:
            return f"{self.PROTOCOL}://{self.DOMAIN}"
        return f"{self.PROTOCOL}://{self.DOMAIN}:{self.PORT}"
    
    # CORS
    BACKEND_CORS_ORIGINS: str = "*"

    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from string"""
        if self.BACKEND_CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]

    # Anime Source Configuration - Individual fields for environment variables
    SAMEHADAKU_BASE_URL: str = "https://v1.samehadaku.how"
    SAMEHADAKU_SEARCH_URL: str = "https://v1.samehadaku.how/"
    SAMEHADAKU_API_URL: str = "https://v1.samehadaku.how/wp-json/custom/v1"
    
    @property
    def ANIME_SOURCES(self) -> Dict[str, Dict[str, Any]]:
        return {
            "samehadaku": {
                "base_url": self.SAMEHADAKU_BASE_URL,
                "search_url": self.SAMEHADAKU_SEARCH_URL,
                "api_url": self.SAMEHADAKU_API_URL,
                "active": True,
            },
            # Tambahkan sumber anime lain di sini
        }

    # Cache Configuration
    CACHE_TTL: int = 600  # 10 menit
    CACHE_LONG_TTL: int = 3600  # 1 jam
    CACHE_VERY_LONG_TTL: int = 86400  # 24 jam

    # Redis Configuration
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Docker Configuration
    NGINX_PORT: int = 80
    NGINX_SSL_PORT: int = 443
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
