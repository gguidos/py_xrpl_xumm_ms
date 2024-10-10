from datetime import datetime
from typing import Dict, Any, List
from src.infrastructure.xrpl import XRPLClient


class XRPLRepository:
    """Repository for performing CRUD operations on the users collection."""

    def __init__(self, client: XRPLClient):
        self.client = client

    def get_account(sefl, seed):
        """Returns the XRPL account"""
        return XRPLClient.get_account(seed)

    def get_account_info(sefl, account_id):
        """Returns the XRPL account info"""
        return XRPLClient.get_account_info(account_id)
    
    def send_xrp(self, seed, amount, destination):
        """Sends XRP"""
        return XRPLClient.send_xrp(seed, amount, destination)
