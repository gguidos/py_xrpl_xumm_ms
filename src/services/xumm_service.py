from src.core.repositories.xumm_repository import XummRepository
from src.core.use_cases.authenticate import Authenticate

class XummService:

    def __init__(self, repository: XummRepository):
        self.xumm_repository = repository
        self.authenticate_use_case = Authenticate(self.xumm_repository)

    async def authenticate(self):
        """Authenticate"""
        return await self.authenticate_use_case.execute()