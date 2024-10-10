from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from redis.asyncio import Redis
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.exception_handlers import register_exception_handlers
from src.middleware.request_id_middleware import RequestIDMiddleware
from src.middleware.logging_middleware import LoggingMiddleware
from src.middleware.response_interceptor import ResponseFormatMiddleware
from src.middleware.security_headers import SecurityHeadersMiddleware
from contextlib import asynccontextmanager
from src.infrastructure.di_container import Container
from src.infrastructure.logging.logging_config import setup_logging
from src.interfaces.api.v1.health_check import router as health_check_router
from src.interfaces.api.v1.xrpl_controller import router as xrpl_router
from src.interfaces.api.v1.xumm_controller import router as xumm_router
from src.middleware.request_id_middleware import RequestIDMiddleware
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Setup logging configuration
setup_logging()

# Initialize the logger
logger = logging.getLogger(__name__)

# Create the FastAPI app
app = FastAPI(
    title="User Management API",
    description="API for managing users in the application",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)
# Register the middleware to intercept all responses
app.add_middleware(ResponseFormatMiddleware)

# Add the Security Headers Middleware
app.add_middleware(SecurityHeadersMiddleware)

# Initialize the DI container
container = Container()

# Set configuration values using environment variables
container.config.db_uri.from_env("MONGO_URI")  # MongoDB URI (e.g., "mongodb://localhost:27017")
container.config.db_name.from_env("DB_NAME")   # Database name (e.g., "mydatabase")
container.config.db_collection.from_env("DB_COLLECTION")  # Collection name (e.g., "users")
container.config.environment.from_env("ENVIRONMENT")  # Environment (development/production)
container.config.api_key.from_env("API_KEY")  # API Key
container.config.xrpl_net_url.from_env("XRPL_NET_URL")
container.config.xumm_api_key.from_env("XUMM_API_KEY")
container.config.xumm_api_secret.from_env("XUMM_API_SECRET")
container.config.rabbitmq_host.from_env("RABBITMQ_HOST")

# Initialize resources to ensure configuration values are fully propagated
container.init_resources()

# Wire the container to the modules that use the dependencies
container.wire(modules=["src.interfaces.api.v1.xrpl_controller"])  # Wire the user controller
container.wire(modules=["src.interfaces.api.v1.xumm_controller"])
# Set the DI container to the app's state (optional if needed for accessing container)
app.container = container
app.state.xrpl_client = container.xrpl_client()
app.state.xumm_client = container.xumm_client()
app.state.rabbitmq_client = container.rabbitmq_client()
# Include health check routes
app.include_router(health_check_router, prefix="/api/v1")

# Include the xrpl and xumm router with dependency injection configured
app.include_router(xrpl_router, prefix="/api/v1", tags=["xrpl"])
app.include_router(xumm_router, prefix="/api/v1", tags=["xumm"])

# Register global exception handlers
register_exception_handlers(app)

# Use an async context manager for lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event manager to handle startup and shutdown events."""
    """Connect to Redis on application startup."""
    global redis
    redis = Redis(host="localhost", port=6379, db=0, encoding="utf-8", decode_responses=True)  # Change host/port as needed
    await FastAPILimiter.init(redis)
    logger.info("Rate Limiter initialized with Redis backend.")
    # Startup event to connect to MongoDB when the application starts
    mongo_client = container.mongo_client()
    await mongo_client.connect()
    logger.info("MongoDB client connected during startup.")

    # Verify that the collection is set correctly
    assert mongo_client.collection is not None, "MongoDB collection is not set during startup"

    # Yield control to allow handling requests
    yield

    # Shutdown event to disconnect from MongoDB when the application shuts down
    await mongo_client.disconnect()
    logger.info("MongoDB client disconnected during shutdown.")
    await redis.close()
    logger.info("Redis connection closed.")

# Set lifespan event handler for the FastAPI application
app.router.lifespan_context = lifespan

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
