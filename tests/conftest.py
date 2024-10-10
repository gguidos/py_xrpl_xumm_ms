# tests/conftest.py

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from src.main import app  # Import the FastAPI app instance from your main.py file
from redis.asyncio import Redis
from fastapi_limiter import FastAPILimiter
from src.infrastructure.di_container import Container

# Set up test configurations
TEST_REDIS_URL = "redis://localhost:6379/1"
TEST_MONGO_URI = "mongodb://localhost:27017"
TEST_DB_NAME = "test_db"
TEST_DB_COLLECTION = "test_users"

#Set up Redis URL for testing
TEST_REDIS_URL = "redis://localhost:6379/1"

@pytest.fixture(scope="module", autouse=True)
async def initialize_test_environment():
    """
    Initialize the test environment by manually initializing necessary dependencies.
    Ensures that all necessary initializations (Redis, MongoDB) are performed.
    """
    # Initialize Redis for rate limiting
    redis = await Redis.from_url(TEST_REDIS_URL, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)  # Explicitly initialize the rate limiter with Redis
    app.state.redis = redis  # Store the redis connection in app state for future use

    # Manually trigger FastAPI's startup event to ensure MongoDB is connected
    await app.router.startup()

    yield  # Run the tests

    # Manually trigger FastAPI's shutdown event
    await app.router.shutdown()
    await redis.close()  # Close Redis connection after tests

@pytest.fixture(scope="module")
async def test_client(initialize_test_environment):
    """
    Fixture to create a test client for the FastAPI app.
    Leverages the initialize_test_environment fixture to ensure all startup/shutdown events are triggered.
    """
    # Create an async test client for the FastAPI app
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
