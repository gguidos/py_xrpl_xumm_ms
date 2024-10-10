from fastapi import HTTPException
from pydantic import ValidationError
from typing import List, Optional
from src.core.entities.user import User
from core.repositories.xrpl_repository import UserRepository
from src.infrastructure.exception_handlers import DuplicateUserException 
from src.core.use_cases.create_user import CreateUser
from src.core.use_cases.get_all_users import GetAllUsers
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

# Conversion functions between Pydantic models and MongoDB documents
def user_to_mongo_dict(user: User) -> dict:
    """Convert a Pydantic User model to a MongoDB dictionary format."""
    return user.model_dump(by_alias=True, exclude_none=True)

def mongo_dict_to_user(mongo_dict: dict) -> User:
    """Convert a MongoDB dictionary to a Pydantic User model."""
    # Convert ObjectId to string for the _id field
    if "_id" in mongo_dict and isinstance(mongo_dict["_id"], ObjectId):
        mongo_dict["_id"] = str(mongo_dict["_id"])
    return User(**mongo_dict)

class UserService:
    """Service layer for managing users."""

    def __init__(self, user_repository: UserRepository, request_id: Optional[str] = None):
        self.user_repository = user_repository
        self.request_id = request_id
        self.create_user_use_case = CreateUser(user_repository)
        self.get_all_users_use_case = GetAllUsers(user_repository)

    async def create_user(self, name: str, email: str, age: int) -> User:
        """Create a new user using the create_user use-case."""
        try:
            logger.info(f"Received request to create user with email: {email}")
            
            # Check if a user with the same email already exists.
            existing_user = await self.find_user_by_email(email=email)
            if existing_user:
                logger.info(f"User with email: {email} already exists.")
                # Raise the custom DuplicateUserException instead of a ValueError
                raise DuplicateUserException(email=email)
            
            # Execute user creation
            created_user = await self.create_user_use_case.execute(name=name, email=email, age=age)
            user_dict = created_user.model_dump()
            logger.info(f"User with email {email} created successfully: {user_dict}")
            return created_user

        except DuplicateUserException as e:
            # Log specific error and raise it to be caught by the global handler
            logger.error(f"Duplicate user error: {e.detail}", extra={"request_id": self.request_id})
            raise e

        except ValidationError as ve:
            # Log Pydantic validation errors
            logger.error(f"Pydantic validation error: {ve.errors()}", extra={"request_id": self.request_id})
            raise HTTPException(status_code=422, detail=ve.errors())

        except Exception as e:
            # Log general exceptions
            logger.error(f"Failed to create user with email {email}: {e}", extra={"request_id": self.request_id})
            raise HTTPException(status_code=500, detail="An error occurred while creating the user")

    async def get_all_users(self) -> List[User]:
        """Get all users using the get_all_users use-case."""
        try:
            return await self.get_all_users_use_case.execute()
        except Exception as e:
            logger.error(f"Failed to retrieve users due to an unexpected error: {str(e)}", exc_info=True)
            # Let the global exception handler handle this
            raise

    async def find_user_by_id(self, user_id: str) -> Optional[User]:
        """Find a user by ID."""
        users = await self.user_repository.find(query={"_id": ObjectId(user_id)})
        if users:
            return User(**users[0])
        return None

    async def find_user_by_email(self, email: str) -> Optional[User]:
        """Find a user by email."""
        users = await self.user_repository.find(query={"email": email})
        if users:
            return User(**users[0])
        return None

    async def find_users_by_age(self, age: int) -> List[User]:
        """Find all users by age."""
        user_data_list = await self.user_repository.find(query={"age": age})
        return [User(**data) for data in user_data_list]

