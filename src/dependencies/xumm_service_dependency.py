from fastapi import Depends
from dependency_injector.wiring import Provide, inject
from src.services.xumm_service import XummService
from src.infrastructure.di_container import Container
from src.dependencies.request_id_dependency import get_request_id
import logging
logger = logging.getLogger(__name__)

@inject
async def get_xumm_service(
    request_id: str = Depends(get_request_id),  # First, get the request ID
    service: XummService = Depends(Provide[Container.xumm_service]) # Get an instance of the DI container
) -> XummService:
    """Create a XummService instance with the provided request_id."""
    logger.debug(f"Creating XummService with request_id: {request_id}")
    # Create a XummService instance and set the request_id dynamically.
    service.request_id = request_id
    logger.debug(f"XummService created: {service}")
    return service
