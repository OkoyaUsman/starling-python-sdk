"""Settle Up API endpoints."""

from typing import Dict, Any


class SettleUpAPI:
    """API for Settle Up-related operations."""

    def __init__(self, client):
        """Initialize with a StarlingClient instance."""
        self.client = client

    def get_profile(self) -> Dict[str, Any]:
        """
        Fetch Settle Up profile for an account holder.

        Requires: settle-up:read OAuth scope

        Returns:
            SettleUpProfile object
        """
        return self.client.get("/api/v2/settle-up/profile")