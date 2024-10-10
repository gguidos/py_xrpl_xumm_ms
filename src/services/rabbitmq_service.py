from typing import List, Optional
from src.core.repositories.rabbitmq_repository import RabbitMQRepository
from src.core.use_cases.rabbitmq.publish_authentication_message import PublishAuthenticationMessage

from bson import ObjectId
import logging

logger = logging.getLogger(__name__)
class RabbitMQService:
    """Service layer for managing RabbitMQ."""

    def __init__(self, repository: RabbitMQRepository, request_id: Optional[str] = None):
        self.repository = repository
        self.request_id = request_id

    def publish_authentication_message(self, user_wallet_address, user_token):
        publish_authentication_message_use_case = PublishAuthenticationMessage(self.repository)
        publish_authentication_message_use_case.execute(user_wallet_address, user_token)