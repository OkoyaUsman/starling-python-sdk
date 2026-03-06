"""Transaction Feed API endpoints."""

from typing import Dict, Any
from datetime import datetime


class FeedAPI:
    """API for transaction feed-related operations."""

    def __init__(self, client):
        """Initialize with a StarlingClient instance."""
        self.client = client

    def get_feed_items(
        self, account_uid: str, category_uid: str, changes_since: datetime
    ) -> Dict[str, Any]:
        """
        Get the account holder's feed items which were created or updated since a given date.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            changes_since: Items which have changed since this timestamp

        Requires: transaction:read OAuth scope

        Returns:
            FeedItems object
        """
        params = {"changesSince": changes_since.isoformat()}
        return self.client.get(
            f"/api/v2/feed/account/{account_uid}/category/{category_uid}", params=params
        )

    def get_transactions_between(
        self,
        account_uid: str,
        category_uid: str,
        min_transaction_timestamp: datetime,
        max_transaction_timestamp: datetime,
    ) -> Dict[str, Any]:
        """
        Get feed items for the specified category, created between two timestamps.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            min_transaction_timestamp: Minimum transaction timestamp
            max_transaction_timestamp: Maximum transaction timestamp

        Requires: transaction:read OAuth scope

        Returns:
            FeedItems object
        """
        params = {
            "minTransactionTimestamp": min_transaction_timestamp.isoformat(),
            "maxTransactionTimestamp": max_transaction_timestamp.isoformat(),
        }
        return self.client.get(
            f"/api/v2/feed/account/{account_uid}/category/{category_uid}/transactions-between",
            params=params,
        )

    def get_settled_transactions_between(
        self,
        account_uid: str,
        min_transaction_timestamp: datetime,
        max_transaction_timestamp: datetime,
    ) -> Dict[str, Any]:
        """
        Get settled feed items for the specified account, with settlement time between two timestamps.

        Args:
            account_uid: Account UID
            min_transaction_timestamp: Minimum transaction timestamp
            max_transaction_timestamp: Maximum transaction timestamp

        Requires: transaction:read OAuth scope

        Returns:
            FeedItems object
        """
        params = {
            "minTransactionTimestamp": min_transaction_timestamp.isoformat(),
            "maxTransactionTimestamp": max_transaction_timestamp.isoformat(),
        }
        return self.client.get(
            f"/api/v2/feed/account/{account_uid}/settled-transactions-between", params=params
        )

    def get_feed_item(
        self, account_uid: str, category_uid: str, feed_item_uid: str
    ) -> Dict[str, Any]:
        """
        Fetch a single feed item.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            feed_item_uid: Feed item UID

        Requires: transaction:read OAuth scope

        Returns:
            FeedItem object
        """
        return self.client.get(
            f"/api/v2/feed/account/{account_uid}/category/{category_uid}/{feed_item_uid}"
        )

    def get_mastercard_details(
        self, account_uid: str, category_uid: str, feed_item_uid: str
    ) -> Dict[str, Any]:
        """
        Fetch additional details about the Mastercard Feed Item.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            feed_item_uid: Feed item UID

        Requires: transaction:read OAuth scope

        Returns:
            MastercardFeedItem object
        """
        return self.client.get(
            f"/api/v2/feed/account/{account_uid}/category/{category_uid}/{feed_item_uid}/mastercard"
        )

    def update_spending_category(
        self,
        account_uid: str,
        category_uid: str,
        feed_item_uid: str,
        spending_category: str,
        permanent_spending_category_update: bool = False,
        previous_spending_category_references_update: bool = False,
    ) -> Dict[str, Any]:
        """
        Change the spending category for a transaction.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            feed_item_uid: Feed item UID
            spending_category: The category of a transaction
            permanent_spending_category_update: Whether to permanently update
            previous_spending_category_references_update: Whether to update previous references

        Requires: transaction:edit OAuth scope

        Returns:
            Empty dict on success
        """
        json_data = {
            "spendingCategory": spending_category,
            "permanentSpendingCategoryUpdate": permanent_spending_category_update,
            "previousSpendingCategoryReferencesUpdate": previous_spending_category_references_update,
        }
        return self.client.put(
            f"/api/v2/feed/account/{account_uid}/category/{category_uid}/{feed_item_uid}/spending-category",
            json_data=json_data,
        )

    def update_user_note(
        self, account_uid: str, category_uid: str, feed_item_uid: str, user_note: str
    ) -> Dict[str, Any]:
        """
        Change the user-specified note attached to a transaction.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            feed_item_uid: Feed item UID
            user_note: User note text

        Requires: transaction:edit OAuth scope

        Returns:
            Empty dict on success
        """
        json_data = {"userNote": user_note}
        return self.client.put(
            f"/api/v2/feed/account/{account_uid}/category/{category_uid}/{feed_item_uid}/user-note",
            json_data=json_data,
        )

    def get_attachments(
        self, account_uid: str, category_uid: str, feed_item_uid: str
    ) -> Dict[str, Any]:
        """
        Fetch the list of items attached to a feed item.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            feed_item_uid: Feed item UID

        Requires: attachment:read OAuth scope

        Returns:
            FeedItemAttachments object
        """
        return self.client.get(
            f"/api/v2/feed/account/{account_uid}/category/{category_uid}/{feed_item_uid}/attachments"
        )

    def upload_attachment(
        self,
        account_uid: str,
        category_uid: str,
        feed_item_uid: str,
        attachment_data: bytes,
        content_type: str,
    ) -> Dict[str, Any]:
        """
        Upload an attachment to a feed item.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            feed_item_uid: Feed item UID
            attachment_data: Attachment data as bytes
            content_type: Content type of the attachment

        Requires: attachment:write OAuth scope

        Returns:
            UUID string of the created attachment
        """
        headers = {"Content-Type": content_type}
        response = self.client._request(
            "POST",
            f"/api/v2/feed/account/{account_uid}/category/{category_uid}/{feed_item_uid}/attachments",
            headers=headers,
            data=attachment_data,
        )
        return response.json()

    def download_attachment(
        self,
        account_uid: str,
        category_uid: str,
        feed_item_uid: str,
        feed_item_attachment_uid: str,
    ) -> bytes:
        """
        Download the feed item attachment.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            feed_item_uid: Feed item UID
            feed_item_attachment_uid: Feed item attachment UID

        Requires: attachment:read OAuth scope

        Returns:
            Attachment data as bytes
        """
        headers = {"Accept": "*/*"}
        response = self.client.get_stream(
            f"/api/v2/feed/account/{account_uid}/category/{category_uid}/{feed_item_uid}/attachments/{feed_item_attachment_uid}",
            headers=headers,
        )
        return response.content

    def get_receipt(
        self, account_uid: str, category_uid: str, feed_item_uid: str
    ) -> Dict[str, Any]:
        """
        Fetch the receipt, created by the registered application, for a given feed item.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            feed_item_uid: Feed item UID

        Requires: receipt:read OAuth scope

        Returns:
            Receipt object
        """
        return self.client.get(
            f"/api/v2/feed/account/{account_uid}/category/{category_uid}/{feed_item_uid}/receipt"
        )

    def get_receipts(
        self, account_uid: str, category_uid: str, feed_item_uid: str
    ) -> Dict[str, Any]:
        """
        Fetch all receipts for a given feed item.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            feed_item_uid: Feed item UID

        Requires: receipts:read OAuth scope

        Returns:
            List of Receipt objects
        """
        return self.client.get(
            f"/api/v2/feed/account/{account_uid}/category/{category_uid}/{feed_item_uid}/receipts"
        )

    def submit_receipt(
        self, account_uid: str, category_uid: str, feed_item_uid: str, receipt: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Submit a receipt for a feed item.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            feed_item_uid: Feed item UID
            receipt: Receipt object

        Requires: receipt:write, metadata:create, or metadata:edit OAuth scope

        Returns:
            ReceiptCreationResponse object
        """
        return self.client.put(
            f"/api/v2/feed/account/{account_uid}/category/{category_uid}/{feed_item_uid}/receipt",
            json_data=receipt,
        )

    # Round-up endpoints
    def get_round_up(self, account_uid: str) -> Dict[str, Any]:
        """
        Returns the round-up goal associated with an account if one has been created.

        Args:
            account_uid: Account UID

        Requires: savings-goal:read OAuth scope

        Returns:
            RoundUpGoalResponse object
        """
        return self.client.get(f"/api/v2/feed/account/{account_uid}/round-up")

    def create_round_up(
        self, account_uid: str, round_up_goal_uid: str, round_up_multiplier: int
    ) -> Dict[str, Any]:
        """
        Activate transaction round-up and adds remainder to savings goal.

        Args:
            account_uid: Account UID
            round_up_goal_uid: UID of the account category to send round-ups to
            round_up_multiplier: How much to multiply the rounded-up amount by (1-10)

        Requires: savings-goal:create OAuth scope

        Returns:
            Empty dict on success
        """
        json_data = {
            "roundUpGoalUid": round_up_goal_uid,
            "roundUpMultiplier": round_up_multiplier,
        }
        return self.client.put(f"/api/v2/feed/account/{account_uid}/round-up", json_data=json_data)

    def delete_round_up(self, account_uid: str) -> Dict[str, Any]:
        """
        Delete the round-up goal associated with an account if one exists.

        Args:
            account_uid: Account UID

        Requires: savings-goal:delete OAuth scope

        Returns:
            Empty dict on success
        """
        return self.client.delete(f"/api/v2/feed/account/{account_uid}/round-up")