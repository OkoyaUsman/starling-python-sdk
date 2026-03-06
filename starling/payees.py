"""Payees API endpoints."""

from typing import Optional, Dict, Any, List
from datetime import date


class PayeesAPI:
    """API for payee-related operations."""

    def __init__(self, client):
        """Initialize with a StarlingClient instance."""
        self.client = client

    def get_payees(self) -> Dict[str, Any]:
        """
        Get an account holder's payees.

        Requires: payee:read OAuth scope

        Returns:
            Payees object containing list of payees
        """
        return self.client.get("/api/v2/payees")

    def get_payee(self, payee_uid: str) -> Dict[str, Any]:
        """
        Get a specific account holder payee.

        Args:
            payee_uid: Unique identifier of the payee

        Requires: payee:read OAuth scope

        Returns:
            Payee object
        """
        return self.client.get(f"/api/v2/payees/{payee_uid}")

    def create_payee(
        self,
        payee_name: str,
        payee_type: str,
        accounts: List[Dict[str, Any]],
        phone_number: Optional[str] = None,
        first_name: Optional[str] = None,
        middle_name: Optional[str] = None,
        last_name: Optional[str] = None,
        business_name: Optional[str] = None,
        date_of_birth: Optional[date] = None,
    ) -> Dict[str, Any]:
        """
        Create a payee.

        Args:
            payee_name: Name of the payee
            payee_type: Type of payee (INDIVIDUAL or BUSINESS)
            accounts: List of payee accounts
            phone_number: Phone number (optional)
            first_name: First name (optional)
            middle_name: Middle name (optional)
            last_name: Last name (optional)
            business_name: Business name (optional)
            date_of_birth: Date of birth (optional)

        Requires: payee:create OAuth scope

        Returns:
            PayeeCreationResponse object
        """
        json_data = {"payeeName": payee_name, "payeeType": payee_type, "accounts": accounts}

        if phone_number:
            json_data["phoneNumber"] = phone_number
        if first_name:
            json_data["firstName"] = first_name
        if middle_name:
            json_data["middleName"] = middle_name
        if last_name:
            json_data["lastName"] = last_name
        if business_name:
            json_data["businessName"] = business_name
        if date_of_birth:
            json_data["dateOfBirth"] = date_of_birth.isoformat()

        return self.client.put("/api/v2/payees", json_data=json_data)

    def update_payee(
        self,
        payee_uid: str,
        payee_name: str,
        payee_type: str,
        accounts: List[Dict[str, Any]],
        phone_number: Optional[str] = None,
        first_name: Optional[str] = None,
        middle_name: Optional[str] = None,
        last_name: Optional[str] = None,
        business_name: Optional[str] = None,
        date_of_birth: Optional[date] = None,
    ) -> Dict[str, Any]:
        """
        Update a payee.

        Args:
            payee_uid: Unique identifier of the payee
            payee_name: Name of the payee
            payee_type: Type of payee (INDIVIDUAL or BUSINESS)
            accounts: List of payee accounts
            phone_number: Phone number (optional)
            first_name: First name (optional)
            middle_name: Middle name (optional)
            last_name: Last name (optional)
            business_name: Business name (optional)
            date_of_birth: Date of birth (optional)

        Requires: payee:edit OAuth scope

        Returns:
            ConsentInformation object
        """
        json_data = {"payeeName": payee_name, "payeeType": payee_type, "accounts": accounts}

        if phone_number:
            json_data["phoneNumber"] = phone_number
        if first_name:
            json_data["firstName"] = first_name
        if middle_name:
            json_data["middleName"] = middle_name
        if last_name:
            json_data["lastName"] = last_name
        if business_name:
            json_data["businessName"] = business_name
        if date_of_birth:
            json_data["dateOfBirth"] = date_of_birth.isoformat()

        return self.client.put(f"/api/v2/payees/{payee_uid}", json_data=json_data)

    def delete_payee(self, payee_uid: str) -> Dict[str, Any]:
        """
        Delete a payee.

        Args:
            payee_uid: Unique identifier of the payee

        Requires: payee:delete OAuth scope

        Returns:
            Empty dict on success
        """
        return self.client.delete(f"/api/v2/payees/{payee_uid}")

    def create_payee_account(
        self,
        payee_uid: str,
        description: str,
        default_account: bool,
        country_code: str,
        account_identifier: str,
        bank_identifier: str,
        bank_identifier_type: str,
        secondary_identifier: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a payee account.

        Args:
            payee_uid: Unique identifier of the payee
            description: Account description
            default_account: Is this the default account for the owning payee
            country_code: Country code (ISO 3166-1 alpha-2)
            account_identifier: The account identifier
            bank_identifier: The bank identifier
            bank_identifier_type: The bank identifier type
            secondary_identifier: Secondary reference data (optional)

        Requires: payee:create OAuth scope

        Returns:
            PayeeAccountCreationResponse object
        """
        json_data = {
            "description": description,
            "defaultAccount": default_account,
            "countryCode": country_code,
            "accountIdentifier": account_identifier,
            "bankIdentifier": bank_identifier,
            "bankIdentifierType": bank_identifier_type,
        }

        if secondary_identifier:
            json_data["secondaryIdentifier"] = secondary_identifier

        return self.client.put(f"/api/v2/payees/{payee_uid}/account", json_data=json_data)

    def delete_payee_account(self, payee_uid: str, account_uid: str) -> Dict[str, Any]:
        """
        Delete a payee account.

        Args:
            payee_uid: Unique identifier of the payee
            account_uid: Unique identifier of the payee account

        Requires: payee:delete OAuth scope

        Returns:
            Empty dict on success
        """
        return self.client.delete(f"/api/v2/payees/{payee_uid}/account/{account_uid}")

    def get_scheduled_payments(self, payee_uid: str, account_uid: str) -> Dict[str, Any]:
        """
        Get scheduled payments.

        Args:
            payee_uid: Unique identifier of the payee
            account_uid: Unique identifier of the payee account

        Requires: scheduled-payment:read OAuth scope

        Returns:
            ScheduledPaymentResponse object
        """
        return self.client.get(f"/api/v2/payees/{payee_uid}/account/{account_uid}/scheduled-payments")

    def get_payments(self, payee_uid: str, account_uid: str, since: date) -> Dict[str, Any]:
        """
        View a history of payments to your payee.

        Args:
            payee_uid: Unique identifier of the payee
            account_uid: Unique identifier of the payee account
            since: Start date for transaction history

        Requires: payee-transaction:read OAuth scope

        Returns:
            Payments object
        """
        params = {"since": since.isoformat()}
        return self.client.get(
            f"/api/v2/payees/{payee_uid}/account/{account_uid}/payments", params=params
        )

    def get_payee_image(self, payee_uid: str) -> bytes:
        """
        Get the image for the payee.

        Args:
            payee_uid: Unique identifier of the payee

        Requires: payee-image:read OAuth scope

        Returns:
            Image data as bytes (PNG format)
        """
        headers = {"Accept": "image/png"}
        response = self.client.get_stream(f"/api/v2/payees/{payee_uid}/image", headers=headers)
        return response.content