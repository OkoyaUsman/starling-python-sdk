"""Accounts API endpoints."""

from typing import Optional, Dict, Any
from datetime import date


class AccountsAPI:
    """API for account-related operations."""

    def __init__(self, client):
        """Initialize with a StarlingClient instance."""
        self.client = client

    def get_accounts(self) -> Dict[str, Any]:
        """
        Get the accounts associated with an account holder.

        Requires: account:read or account-list:read OAuth scope

        Returns:
            Accounts object containing list of accounts
        """
        return self.client.get("/api/v2/accounts")

    def get_balance(self, account_uid: str) -> Dict[str, Any]:
        """
        Get an account's balance.

        Args:
            account_uid: Account UID

        Requires: balance:read OAuth scope

        Returns:
            BalanceV2 object with balance details
        """
        return self.client.get(f"/api/v2/accounts/{account_uid}/balance")

    def get_identifiers(self, account_uid: str) -> Dict[str, Any]:
        """
        Get an account's bank identifiers.

        Args:
            account_uid: Account UID

        Requires: account-identifier:read OAuth scope

        Returns:
            AccountIdentifiers object with bank and account identifiers
        """
        return self.client.get(f"/api/v2/accounts/{account_uid}/identifiers")

    def get_confirmation_of_funds(
        self, account_uid: str, target_amount_in_minor_units: int
    ) -> Dict[str, Any]:
        """
        Get whether there are available funds for a requested amount.

        Args:
            account_uid: Account UID
            target_amount_in_minor_units: Target amount in minor units

        Requires: confirmation-of-funds:read OAuth scope

        Returns:
            ConfirmationOfFundsResponse object
        """
        params = {"targetAmountInMinorUnits": target_amount_in_minor_units}
        return self.client.get(
            f"/api/v2/accounts/{account_uid}/confirmation-of-funds", params=params
        )

    def download_feed_export(
        self,
        account_uid: str,
        start: date,
        end: Optional[date] = None,
    ) -> bytes:
        """
        Download a Feed Export for a given date range.

        Args:
            account_uid: Account UID
            start: Start date for the export
            end: End date for the export (optional)

        Requires: feed-export-csv:read OAuth scope

        Returns:
            CSV data as bytes
        """
        params = {"start": start.isoformat()}
        if end:
            params["end"] = end.isoformat()

        headers = {"Accept": "text/csv"}
        response = self.client.get_stream(
            f"/api/v2/accounts/{account_uid}/feed-export",
            params=params,
            headers=headers,
        )
        return response.content