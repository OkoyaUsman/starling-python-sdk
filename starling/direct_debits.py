"""Direct Debit Mandates API endpoints."""

from typing import Dict, Any
from datetime import date


class DirectDebitsAPI:
    """API for direct debit mandate-related operations."""

    def __init__(self, client):
        """Initialize with a StarlingClient instance."""
        self.client = client

    def get_mandates(self) -> Dict[str, Any]:
        """
        Get a list of direct debit mandates.

        Requires: mandate:read OAuth scope

        Returns:
            DirectDebitMandatesV2 object containing list of mandates
        """
        return self.client.get("/api/v2/direct-debit/mandates")

    def get_mandate(self, mandate_uid: str) -> Dict[str, Any]:
        """
        Get the direct debit mandate with the specified identifier.

        Args:
            mandate_uid: Unique identifier of the mandate

        Requires: mandate:read OAuth scope

        Returns:
            DirectDebitMandateV2 object
        """
        return self.client.get(f"/api/v2/direct-debit/mandates/{mandate_uid}")

    def get_mandates_for_account(self, account_uid: str) -> Dict[str, Any]:
        """
        Get a list of direct debit mandates for an account.

        Args:
            account_uid: Unique identifier of the account

        Requires: mandate:read OAuth scope

        Returns:
            DirectDebitMandatesV2 object containing list of mandates
        """
        return self.client.get(f"/api/v2/direct-debit/mandates/account/{account_uid}")

    def get_mandate_payments(self, mandate_uid: str, since: date) -> Dict[str, Any]:
        """
        Get a transaction history for a direct debit.

        Args:
            mandate_uid: Unique identifier of the mandate
            since: Start date for transaction history

        Requires: mandate:read OAuth scope

        Returns:
            DirectDebitPaymentsResponse object
        """
        params = {"since": since.isoformat()}
        return self.client.get(f"/api/v2/direct-debit/mandates/{mandate_uid}/payments", params=params)

    def cancel_mandate(self, mandate_uid: str) -> Dict[str, Any]:
        """
        Cancel the direct debit mandate with the specified identifier.

        Args:
            mandate_uid: Unique identifier of the mandate

        Requires: mandate:delete OAuth scope

        Returns:
            Empty dict on success
        """
        return self.client.delete(f"/api/v2/direct-debit/mandates/{mandate_uid}")