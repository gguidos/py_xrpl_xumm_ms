from dependency_injector import containers, providers
from src.infrastructure.db.mongo_client import MongoDBClient
from core.repositories.xrpl_repository import UserRepository
from src.services.user_service import UserService

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Set up the MongoDB client using a Singleton provider
    mongo_client = providers.Singleton(
        MongoDBClient,
        db_uri=config.db_uri,
        db_name=config.db_name,
        db_collection=config.db_collection  # Make sure you are using the correct attribute names
    )

    # Register UserRepository with the MongoDB client
    user_repository = providers.Factory(
        UserRepository,
        client=mongo_client
    )

    # Register UserService with UserRepository
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository
    )

