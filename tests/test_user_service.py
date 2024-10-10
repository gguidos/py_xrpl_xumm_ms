# import pytest
# from src.services.user_service import UserService
# from src.core.entities.user import User
# from src.core.repositories.user_repository import UserRepository

# @pytest.fixture
# def mock_user_repository():
#     """Create a mock UserRepository."""
#     class MockUserRepository(UserRepository):
#         async def find(self, query):
#             if query.get("email") == "exists@example.com":
#                 return [User(name="Existing User", email="exists@example.com", age=30)]
#             return []

#         async def create(self, user_data):
#             return "mock_id"
#     return MockUserRepository(None)

# @pytest.fixture
# def user_service(mock_user_repository):
#     """Create a UserService instance using the mock repository."""
#     return UserService(user_repository=mock_user_repository)

# @pytest.mark.anyio
# async def test_create_user(user_service):
#     new_user = await user_service.create_user(name="John Doe", email="john@example.com", age=25)
#     assert new_user.name == "John Doe"
#     assert new_user.email == "john@example.com"
#     assert new_user.age == 25

# @pytest.mark.anyio
# async def test_create_existing_user(user_service):
#     with pytest.raises(ValueError) as exc_info:
#         await user_service.create_user(name="Existing User", email="exists@example.com", age=30)
#     assert str(exc_info.value) == "User with email exists@example.com already exists."
