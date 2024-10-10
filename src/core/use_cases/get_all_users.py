# src/core/use_cases/get_all_users.py

from typing import List
from src.core.entities.user import User
from core.repositories.xrpl_repository import UserRepository

class GetAllUsers:
    """Use-case for getting all users."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self) -> List[User]:
        """Execute the use-case to get all users."""
        # Call the repository method to get all users and return them as a list of User entities
        documents = await self.user_repository.find_all()
        return [User(**doc) for doc in documents]  # Convert each document to a User entity
