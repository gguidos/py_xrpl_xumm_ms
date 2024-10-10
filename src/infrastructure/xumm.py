from fastapi import HTTPException
import xumm
import logging

# Initialize logging
logger = logging.getLogger(__name__)

class XummClient:
    def __init__(self, api_key: str, api_secret: str):
        self.sdk = xumm.XummSdk(api_key, api_secret)

    async def create_payload(self, payload: dict) -> dict:
        """Create a payload for a Xumm request."""
        try:
            xumm_response = self.sdk.payload.create(payload)
            
            # Extract the refs attributes as a dictionary (manually, or using __dict__ if possible)
            refs_dict = {
                "qr_png": xumm_response.refs.qr_png,
                "qr_matrix": xumm_response.refs.qr_matrix,
                "qr_uri_quality_opts": getattr(xumm_response.refs, "qr_uri_quality_opts", None),  # Use getattr in case it's optional
            }
            return {
                "next": xumm_response.next.always,
                "uuid": xumm_response.uuid,
                "refs": refs_dict
            }
        except Exception as e:
            logger.error(f"Error creating Xumm request: {e}")
            raise HTTPException(status_code=500, detail="Failed to create Xumm request")
        
    async def get_payload(self, uuid: str) -> dict:
        """Get payload details using its UUID."""
        try:
            return self.sdk.payload.get(uuid)
        except Exception as e:
            logger.error(f"Error getting Xumm request: {e}")
            raise HTTPException(status_code=500, detail="Failed to get Xumm request")
