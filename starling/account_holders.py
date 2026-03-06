"""Account Holders API endpoints."""

from typing import Dict, Any


class AccountHoldersAPI:
    """API for account holder-related operations."""

    def __init__(self, client):
        """Initialize with a StarlingClient instance."""
        self.client = client

    def get_account_holder(self) -> Dict[str, Any]:
        """
        Get basic information about the account holder.

        Requires: customer:read or account-holder-type:read OAuth scope

        Returns:
            AccountHolder object
        """
        return self.client.get("/api/v2/account-holder")

    def get_account_holder_name(self) -> Dict[str, Any]:
        """
        Get the name of the account holder.

        Requires: account-holder-name:read OAuth scope

        Returns:
            AccountHolderName object
        """
        return self.client.get("/api/v2/account-holder/name")

    # Business endpoints
    def get_business(self) -> Dict[str, Any]:
        """
        Get a business account holder's details.

        Requires: account:read OAuth scope

        Returns:
            Business object
        """
        return self.client.get("/api/v2/account-holder/business")

    def get_business_correspondence_address(self) -> Dict[str, Any]:
        """
        Get a company's correspondence address.

        Requires: address:read OAuth scope

        Returns:
            AddressV2 object
        """
        return self.client.get("/api/v2/account-holder/business/correspondence-address")

    def get_business_registered_address(self) -> Dict[str, Any]:
        """
        Get a company's registered address.

        Requires: address:read OAuth scope

        Returns:
            AddressV2 object
        """
        return self.client.get("/api/v2/account-holder/business/registered-address")

    # Individual endpoints
    def get_individual(self) -> Dict[str, Any]:
        """
        Get an individual account holder's details.

        Requires: customer:read OAuth scope

        Returns:
            Individual object
        """
        return self.client.get("/api/v2/account-holder/individual")

    def update_individual_email(self, email: str) -> Dict[str, Any]:
        """
        Update an individual account holder's email address.

        Args:
            email: The new email address

        Requires: message signing and email:edit OAuth scope

        Returns:
            Empty dict on success
        """
        json_data = {"email": email}
        return self.client.put("/api/v2/account-holder/individual/email", json_data=json_data)

    # Joint account endpoints
    def get_joint(self) -> Dict[str, Any]:
        """
        Get a joint account holder's details.

        Requires: customer:read OAuth scope

        Returns:
            JointAccount object
        """
        return self.client.get("/api/v2/account-holder/joint")

    # Sole trader endpoints
    def get_sole_trader(self) -> Dict[str, Any]:
        """
        Get sole trader business details.

        Requires: account:read OAuth scope

        Returns:
            SoleTrader object
        """
        return self.client.get("/api/v2/account-holder/sole-trader")

    # Profile image endpoints
    def get_profile_image(self, account_holder_uid: str) -> bytes:
        """
        Get a profile image if one exists.

        Args:
            account_holder_uid: Unique identifier of an account holder

        Requires: profile-image:read OAuth scope

        Returns:
            Image data as bytes
        """
        headers = {"Accept": "image/*"}
        response = self.client.get_stream(
            f"/api/v2/account-holder/{account_holder_uid}/profile-image",
            headers=headers,
        )
        return response.content

    def update_profile_image(
        self, account_holder_uid: str, image_data: bytes, content_type: str = "image/jpeg"
    ) -> Dict[str, Any]:
        """
        Update a profile image if one already exists.

        Args:
            account_holder_uid: Unique identifier of an account holder
            image_data: Image data as bytes
            content_type: Content type of the image (default: image/jpeg)

        Requires: profile-image:edit OAuth scope

        Returns:
            Empty dict on success
        """
        headers = {"Content-Type": content_type}
        response = self.client._request(
            "PUT",
            f"/api/v2/account-holder/{account_holder_uid}/profile-image",
            headers=headers,
            data=image_data,
        )
        if response.status_code == 204:
            return {}
        return response.json() if response.content else {}

    def delete_profile_image(self, account_holder_uid: str) -> Dict[str, Any]:
        """
        Delete a profile image if one exists.

        Args:
            account_holder_uid: Unique identifier of an account holder

        Requires: profile-image:edit OAuth scope

        Returns:
            Empty dict on success
        """
        return self.client.delete(f"/api/v2/account-holder/{account_holder_uid}/profile-image")