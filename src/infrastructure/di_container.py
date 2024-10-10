from dependency_injector import containers, providers
from src.infrastructure.db.redis_client import RedisClient
from src.infrastructure.db.mongo_client import MongoDBClient
from src.infrastructure.pika import PikaClient
from src.infrastructure.xrpl import XRPLClient
from src.infrastructure.xumm import XummClient
from src.core.repositories.db_repository import DBRepository
from src.core.repositories.xrpl_repository import XRPLRepository
from src.core.repositories.xumm_repository import XummRepository
from src.core.repositories.rabbitmq_repository import RabbitMQRepository
from src.services.xrpl_service import XRPLService
from src.services.xumm_service import XummService
from src.services.rabbitmq_service import RabbitMQService

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Clients

    # MongoDB Client (Singleton)
    mongo_client = providers.Singleton(
        MongoDBClient,
        db_uri=config.db_uri,
        db_name=config.db_name,
        db_collection=config.db_collection
    )

    # RabbitMQ Client (Singleton)
    rabbitmq_client = providers.Singleton(
        PikaClient,
        rabbitmq_host=config.rabbitmq_host
    )

    # Redis Client (Singleton)
    redis_client = providers.Singleton(
        RedisClient,
        host=config.redis_host,
        port=config.redis_port,
        db=config.redis_db,
        password=config.redis_password
    )

    # Xumm Client (Factory)
    xumm_client = providers.Factory(
        XummClient,
        api_key=config.xumm_api_key,
        api_secret=config.xumm_api_secret
    )

    # XRPL Client (Singleton)
    xrpl_client = providers.Singleton(
        XRPLClient,
        xrpl_net_url=config.xrpl_net_url
    )

    # Repositories

    db_repository = providers.Factory(
        DBRepository,
        client=mongo_client
    )

    rabbitmq_repository = providers.Factory(
        RabbitMQRepository,
        pika_client=rabbitmq_client
    )

    xrpl_repository = providers.Factory(
        XRPLRepository,
        client=xrpl_client
    )

    xumm_repository = providers.Factory(
        XummRepository,
        client=xumm_client
    )

    # Services

    xrpl_service = providers.Factory(
        XRPLService,
        repository=xrpl_repository
    )

    xumm_service = providers.Factory(
        XummService,
        repository=xumm_repository
    )

    rabbitmq_service = providers.Factory(
        RabbitMQService,
        repository=rabbitmq_repository
    )
