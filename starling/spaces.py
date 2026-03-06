"""Spaces API endpoints."""

from typing import Dict, Any


class SpacesAPI:
    """API for spaces-related operations."""

    def __init__(self, client):
        """Initialize with a StarlingClient instance."""
        self.client = client

    def get_spaces(self, account_uid: str) -> Dict[str, Any]:
        """
        Get all active savings and spending spaces.

        Args:
            account_uid: Account UID

        Requires: space:read OAuth scope

        Returns:
            Spaces object
        """
        return self.client.get(f"/api/v2/account/{account_uid}/spaces")

    def get_spending_space(self, account_uid: str, space_uid: str) -> Dict[str, Any]:
        """
        Get a spending space.

        Args:
            account_uid: Account UID
            space_uid: Spending space UID

        Requires: space:read OAuth scope

        Returns:
            SpendingSpace object
        """
        return self.client.get(f"/api/v2/account/{account_uid}/spaces/spending/{space_uid}")

    def get_space_photo(self, account_uid: str, space_uid: str) -> Dict[str, Any]:
        """
        Get the photo associated with a space.

        Args:
            account_uid: Account UID
            space_uid: Space UID

        Requires: space:read OAuth scope

        Returns:
            SpacePhoto object
        """
        return self.client.get(f"/api/v2/account/{account_uid}/spaces/{space_uid}/photo")