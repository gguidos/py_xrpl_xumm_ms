# src/core/use_cases/create_user.py

from src.core.entities.user import User
from core.repositories.xrpl_repository import UserRepository

class CreateUser:
    """Use-case for creating a new user."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, name: str, email: str, age: int) -> User:
        """Create a new user and return the created user."""
        user = User(name=name, email=email, age=age)
        user_id = await self.user_repository.create(user.dict(by_alias=True))
        user.id = user_id
        return user
