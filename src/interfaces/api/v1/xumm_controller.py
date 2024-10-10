from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from typing import List, Dict, Any
from src.dependencies.api_key_dependency import get_api_key
from src.dependencies.xumm_service_dependency import get_xumm_service
from src.dependencies.rabbitmq_service_dependency import get_rabbitmq_service
from src.services.xumm_service import XummService
from src.services.rabbitmq_service import RabbitMQService
from src.infrastructure.di_container import Container
import logging

logger = logging.getLogger(__name__)
# Create a FastAPI router for user-related endpoints
router = APIRouter()

# Get configuration from the container to conditionally include dependencies
container = Container()

# Conditionally add API key protection based on environment
api_key_dependency = Depends(get_api_key) if container.config.environment() != "development" else None

@router.get("/xumm/auth/",
            response_model=Any,
            dependencies=[
                Depends(RateLimiter(times=2, seconds=4))])
async def authenticate(
    service: XummService = Depends(get_xumm_service)  # Use Provide to inject UserService from Container
):
    """Authenticate"""
    return await service.authenticate()

@router.post("/xumm/webhook", tags=["Authentication"])
async def xumm_webhook(
    request: Request,
    rabbitmq_service: RabbitMQService = Depends(get_rabbitmq_service)):
    try:
        data = await request.json()
        logger.info("Received webhook callback from Xumm")

        

        # Extract signing information from 'payloadResponse'
        if data.get("payloadResponse", {}).get("signed"):
            user_wallet_address = data["payloadResponse"].get("txid")
            user_token = data["userToken"].get("user_token") if "userToken" in data else None
            # Debugging: Print the actual payload received
            logger.info(f"Webhook payload: {user_token}")

            # Publish authentication message to RabbitMQ
            rabbitmq_service.publish_authentication_message(user_wallet_address, user_token)

            logger.info(f"User signed in successfully with wallet address/txid: {user_wallet_address}")
            return {"detail": "User authenticated successfully", "wallet_address": user_wallet_address}
        else:
            logger.warning("User did not complete the sign-in successfully")
            return {"detail": "User did not complete sign-in successfully"}
    except Exception as e:
        logger.error(f"Error handling Xumm webhook: {e}")
        raise HTTPException(status_code=500, detail="Failed to handle Xumm webhook")