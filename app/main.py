import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import time

from .api.api import api_router
from .core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("app.main")

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware for logging requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = (time.time() - start_time) * 1000
    logger.info(f"Response: {response.status_code} ({process_time:.2f}ms)")
    
    return response

# Add exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

def custom_openapi(request: Request):
    """Generate OpenAPI schema with dynamic server URLs"""
    if app.openapi_schema:
        return app.openapi_schema
    
    # Get current request info
    scheme = request.url.scheme
    host = request.headers.get("host", str(request.url.netloc))
    
    # Check for forwarded headers (for reverse proxy/load balancer)
    forwarded_proto = request.headers.get("x-forwarded-proto")
    forwarded_host = request.headers.get("x-forwarded-host")
    
    if forwarded_proto:
        scheme = forwarded_proto
    if forwarded_host:
        host = forwarded_host
    
    # Use configured domain if available, otherwise use request host
    if hasattr(settings, 'DOMAIN') and settings.DOMAIN != "localhost":
        host = settings.DOMAIN
        scheme = getattr(settings, 'PROTOCOL', scheme)
    
    server_url = f"{scheme}://{host}"
    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description=f"FastAPI Anime Scraping API - Dynamic host: {server_url}",
        routes=app.routes,
        servers=[
            {"url": server_url, "description": "Current server"},
            {"url": f"{scheme}://{host}{settings.API_V1_STR}", "description": "API v1"}
        ]
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request):
    """Custom Swagger UI with dynamic OpenAPI URL"""
    # Reset openapi_schema to ensure fresh generation
    app.openapi_schema = None
    
    return get_swagger_ui_html(
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        title=f"{settings.PROJECT_NAME} - Swagger UI",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

@app.get(f"{settings.API_V1_STR}/openapi.json", include_in_schema=False)
async def get_openapi_endpoint(request: Request):
    """Dynamic OpenAPI JSON endpoint"""
    return custom_openapi(request)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    logger.warning(f"Could not mount static files: {e}")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to KortekStream API"}

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}