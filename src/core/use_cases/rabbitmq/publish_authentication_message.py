import logging
from src.core.repositories.rabbitmq_repository import RabbitMQRepository

logger = logging.getLogger(__name__)

class PublishAuthenticationMessage:
    def __init__(self, repository: RabbitMQRepository):
        self.repository = repository

    def execute(self, user_wallet_address, user_token):
        try:
            # Construct the message payload as a dictionary
            message = {
                "user_wallet_address": user_wallet_address,
                "user_token": user_token,
                "status": "authenticated"
            }

            # Use the repository to publish the message
            self.repository.publish_auth_message(message)
        except Exception as e:
            logger.error(f"Failed to publish authentication message: {e}")
            raise