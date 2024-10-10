from src.core.repositories.xumm_repository import XummRepository

class Authenticate:
    def __init__(self, xumm_repository: XummRepository):
        self.xumm_repository = xumm_repository

    async def execute(self):
        """Authenticate"""
        payload = {
            "txjson": {
                "TransactionType": "SignIn"
            },
            "options": {
                "pathfinding_fallback": False
            }
        }

        return await self.xumm_repository.create_payload(payload)