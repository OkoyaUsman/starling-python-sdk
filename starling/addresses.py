"""Addresses API endpoints."""

from typing import Optional, Dict, Any
from datetime import date


class AddressesAPI:
    """API for address-related operations."""

    def __init__(self, client):
        """Initialize with a StarlingClient instance."""
        self.client = client

    def get_addresses(self) -> Dict[str, Any]:
        """
        Get the account holder's addresses.

        Requires: address:read OAuth scope

        Returns:
            AddressesV2 object with current and previous addresses
        """
        return self.client.get("/api/v2/addresses")

    def update_address(
        self,
        line1: str,
        post_town: str,
        post_code: str,
        country_code: str,
        line2: Optional[str] = None,
        line3: Optional[str] = None,
        udprn: Optional[str] = None,
        umprn: Optional[str] = None,
        from_date: Optional[date] = None,
    ) -> Dict[str, Any]:
        """
        Update the account holder's current address.

        Args:
            line1: First line of address
            post_town: Post town
            post_code: Post code
            country_code: Country code (ISO 3166-1 alpha-2, e.g., GB)
            line2: Second line of address (optional)
            line3: Third line of address (optional)
            udprn: UDPRN of the property (optional)
            umprn: UMPRN of the property (optional)
            from_date: Date residency started (optional)

        Requires: message signing and address:edit OAuth scope

        Returns:
            Empty dict on success
        """
        json_data = {
            "line1": line1,
            "postTown": post_town,
            "postCode": post_code,
            "countryCode": country_code,
        }

        if line2:
            json_data["line2"] = line2
        if line3:
            json_data["line3"] = line3
        if udprn:
            json_data["udprn"] = udprn
        if umprn:
            json_data["umprn"] = umprn
        if from_date:
            json_data["from"] = from_date.isoformat()

        return self.client.post("/api/v2/addresses", json_data=json_data)