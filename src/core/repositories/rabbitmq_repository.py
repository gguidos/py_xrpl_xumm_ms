import logging
import json
from src.infrastructure.pika import PikaClient

logger = logging.getLogger(__name__)

class RabbitMQRepository:
    def __init__(self, pika_client: PikaClient):
        self.pika_client = pika_client

    def publish_auth_message(self, message):
        """Publish an authentication message to the auth queue"""
        try:
            queue_name = 'user_auth_queue'

            # Ensure message is a JSON string
            if isinstance(message, dict):
                message = json.dumps(message)

            self.pika_client.basic_publish(queue_name, message)
            logger.info(f"Published authentication message to queue '{queue_name}'")
        except Exception as e:
            logger.error(f"Error publishing auth message: {e}")
            raise

    def publish_message(self, queue_name, message):
        """Publish a message to a specific RabbitMQ queue"""
        try:
            self.pika_client.basic_publish(queue_name, message)
            logger.info(f"Published message to queue '{queue_name}'")
        except Exception as e:
            logger.error(f"Error publishing message to queue '{queue_name}': {e}")
            raise

    def purge_queue(self, queue_name):
        """Purge messages from a given RabbitMQ queue"""
        try:
            self.pika_client.purge_queue(queue_name)
            logger.info(f"Purged queue '{queue_name}'")
        except Exception as e:
            logger.error(f"Error purging queue '{queue_name}': {e}")
            raise

    def delete_queue(self, queue_name):
        """Delete a given RabbitMQ queue"""
        try:
            self.pika_client.delete_queue(queue_name)
            logger.info(f"Deleted queue '{queue_name}'")
        except Exception as e:
            logger.error(f"Error deleting queue '{queue_name}': {e}")
            raise
