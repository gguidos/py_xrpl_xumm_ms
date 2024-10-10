from fastapi import Depends
from dependency_injector.wiring import Provide, inject
from src.services.xrpl_service import XRPLService
from src.infrastructure.di_container import Container
from src.dependencies.request_id_dependency import get_request_id
import logging
logger = logging.getLogger(__name__)

@inject
async def get_xrpl_service(
    request_id: str = Depends(get_request_id),  # First, get the request ID
    user_service: XRPLService = Depends(Provide[Container.xrpl_service]) # Get an instance of the DI container
) -> XRPLService:
    """Create a XRPLService instance with the provided request_id."""
    logger.debug(f"Creating XRPLService with request_id: {request_id}")
    # Create a XRPLService instance and set the request_id dynamically.
    user_service.request_id = request_id
    logger.debug(f"XRPLService created: {user_service}")
    return user_service
