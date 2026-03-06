"""Identity API endpoints."""

from typing import Dict, Any


class IdentityAPI:
    """API for identity-related operations."""

    def __init__(self, client):
        """Initialize with a StarlingClient instance."""
        self.client = client

    def get_token_identity(self) -> Dict[str, Any]:
        """
        Get current token identity.

        Returns information about permissions, token expiration, and account holder identifier.

        Requires: OAuth access token (no scopes required)

        Returns:
            IdentityV2 object
        """
        return self.client.get("/api/v2/identity/token")

    def get_individual(self) -> Dict[str, Any]:
        """
        Get the individual who authorised the application.

        Requires: authorising-individual:read OAuth scope

        Returns:
            Individual object
        """
        return self.client.get("/api/v2/identity/individual")

    def logout(self) -> Dict[str, Any]:
        """
        Logout the current individual.

        This endpoint logs an individual out by disabling all of their active access tokens.

        Requires: OAuth access token (no scopes required)

        Returns:
            Empty dict on success (202 Accepted)
        """
        return self.client.put("/api/v2/identity/logout")