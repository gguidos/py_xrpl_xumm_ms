from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from typing import List, Dict, Any
from src.dependencies.api_key_dependency import get_api_key
from src.services.xrpl_service import XRPLService
from src.dependencies.xrpl_service_dependency import get_xrpl_service
from src.infrastructure.di_container import Container

# Create a FastAPI router for user-related endpoints
router = APIRouter()

# Get configuration from the container to conditionally include dependencies
container = Container()

# Conditionally add API key protection based on environment
api_key_dependency = Depends(get_api_key) if container.config.environment() != "development" else None

@router.get("/xrpl/account/",
            response_model=dict,
            dependencies=[
                Depends(RateLimiter(times=2, seconds=4))])
async def get_account(
    service: XRPLService = Depends(get_xrpl_service)  # Use Provide to inject UserService from Container
):
    """Get account."""
    return await service.get_account()