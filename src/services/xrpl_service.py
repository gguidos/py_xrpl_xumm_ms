from typing import List, Optional
from src.core.repositories.xrpl_repository import XRPLRepository

from bson import ObjectId
import logging

logger = logging.getLogger(__name__)
class XRPLService:
    """Service layer for managing XRPL."""

    def __init__(self, repository: XRPLRepository, request_id: Optional[str] = None):
        self.repository = repository
        self.request_id = request_id
