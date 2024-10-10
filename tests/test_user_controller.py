import pytest
import logging
from httpx import AsyncClient
from src.main import app  # Ensure that you are importing the FastAPI app

# Enable logging for tests
logging.basicConfig(level=logging.ERROR)

@pytest.fixture(scope="module")
async def test_client():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client

@pytest.mark.anyio
async def test_get_all_users(test_client):
    # Use logging to verify the test setup and request
    logging.info("Sending GET request to /api/v1/users/")
    
    response = await test_client.get("/api/v1/users/")
    logging.info(f"Received response: {response.status_code} - {response.text}")
    
    assert response.status_code == 200

# @pytest.mark.anyio
# async def test_create_user(test_client):
#     user_payload = {"name": "John Doe", "email": "john.test@example.com", "age": 25}
#     response = await test_client.post("/api/v1/users/", json=user_payload)
#     assert response.status_code == 200
#     assert response.json()["name"] == "John Doe"
