from fastapi import Depends
from src.services.rabbitmq_service import RabbitMQService
from dependency_injector.wiring import Provide, inject
from src.infrastructure.di_container import Container
from src.dependencies.request_id_dependency import get_request_id

import logging
logger = logging.getLogger(__name__)

@inject
async def get_rabbitmq_service(
    request_id: str = Depends(get_request_id),  # First, get the request ID
    service: RabbitMQService = Depends(Provide[Container.rabbitmq_service]) # Get an instance of the DI container
) -> RabbitMQService:
    """Create a RabbitMQService instance with the provided request_id."""
    logger.debug(f"Creating RabbitMQService with request_id: {request_id}")
    # Create a RabbitMQService instance and set the request_id dynamically.
    service.request_id = request_id
    logger.debug(f"RabbitMQService created: {service}")
    return service