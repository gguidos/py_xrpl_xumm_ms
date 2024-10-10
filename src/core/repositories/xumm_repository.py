from src.infrastructure.xumm import XummClient

class XummRepository:

    def __init__(self, client: XummClient):
        self.xumm_client = client

    async def create_payload(self, payload: dict) -> dict:
        """Create a Xumm payload and return its response data."""
        return await self.xumm_client.create_payload(payload)

    async def get_payload(self, uuid: str) -> dict:
        """Retrieve details of a Xumm payload by UUID."""
        return await self.xumm_client.get_payload(uuid)
