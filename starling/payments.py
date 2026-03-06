"""Payments API endpoints."""

from typing import Optional, Dict, Any


class PaymentsAPI:
    """API for payment-related operations."""

    def __init__(self, client):
        """Initialize with a StarlingClient instance."""
        self.client = client

    def create_payment(
        self,
        account_uid: str,
        category_uid: str,
        external_identifier: str,
        reference: str,
        amount: Dict[str, Any],
        destination_payee_account_uid: Optional[str] = None,
        payment_recipient: Optional[Dict[str, Any]] = None,
        spending_category: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create and send an immediate payment within the UK under the Faster Payments Scheme or via SEPA.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            external_identifier: Unique identifier for idempotency
            reference: Payment reference (max 18 chars for FPS, 35 for SEPA)
            amount: CurrencyAndAmount object
            destination_payee_account_uid: Payee account UID (optional)
            payment_recipient: PaymentRecipient object (optional)
            spending_category: Spending category (optional)

        Requires: message signing and pay-local:create or pay-local-once:create OAuth scope

        Returns:
            InstructLocalPaymentResponse object
        """
        json_data = {
            "externalIdentifier": external_identifier,
            "reference": reference,
            "amount": amount,
        }

        if destination_payee_account_uid:
            json_data["destinationPayeeAccountUid"] = destination_payee_account_uid
        if payment_recipient:
            json_data["paymentRecipient"] = payment_recipient
        if spending_category:
            json_data["spendingCategory"] = spending_category

        return self.client.put(
            f"/api/v2/payments/local/account/{account_uid}/category/{category_uid}",
            json_data=json_data,
        )

    def get_payment_order(self, payment_order_uid: str) -> Dict[str, Any]:
        """
        Get a payment order.

        Args:
            payment_order_uid: Payment order UID

        Requires: pay-local:read OAuth scope

        Returns:
            PaymentOrderV2 object
        """
        return self.client.get(f"/api/v2/payments/local/payment-order/{payment_order_uid}")

    def get_payment_order_payments(self, payment_order_uid: str) -> Dict[str, Any]:
        """
        Get the payments associated with a payment order.

        Args:
            payment_order_uid: Payment order UID

        Requires: pay-local:read OAuth scope

        Returns:
            PaymentOrderPaymentsResponse object
        """
        return self.client.get(
            f"/api/v2/payments/local/payment-order/{payment_order_uid}/payments"
        )

    # Standing Orders
    def get_standing_orders(self, account_uid: str, category_uid: str) -> Dict[str, Any]:
        """
        List standing orders.

        Args:
            account_uid: Account UID
            category_uid: Category UID

        Requires: standing-order:read or standing-order-own:read OAuth scope

        Returns:
            StandingOrdersResponse object
        """
        return self.client.get(
            f"/api/v2/payments/local/account/{account_uid}/category/{category_uid}/standing-orders"
        )

    def get_standing_order(
        self, account_uid: str, category_uid: str, payment_order_uid: str
    ) -> Dict[str, Any]:
        """
        Get a standing order.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            payment_order_uid: Payment Order UID

        Requires: standing-order:read or standing-order-own:read OAuth scope

        Returns:
            StandingOrder object
        """
        return self.client.get(
            f"/api/v2/payments/local/account/{account_uid}/category/{category_uid}/standing-orders/{payment_order_uid}"
        )

    def create_standing_order(
        self,
        account_uid: str,
        category_uid: str,
        external_identifier: str,
        reference: str,
        amount: Dict[str, Any],
        standing_order_recurrence: Dict[str, Any],
        destination_payee_account_uid: Optional[str] = None,
        payment_recipient: Optional[Dict[str, Any]] = None,
        spending_category: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new standing order.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            external_identifier: Unique identifier for idempotency
            reference: Payment reference
            amount: CurrencyAndAmount object
            standing_order_recurrence: StandingOrderRecurrence object
            destination_payee_account_uid: Payee account UID (optional)
            payment_recipient: PaymentRecipient object (optional)
            spending_category: Spending category (optional)

        Requires: message signing and standing-order:create OAuth scope

        Returns:
            CreateStandingOrderResponse object
        """
        json_data = {
            "externalIdentifier": external_identifier,
            "reference": reference,
            "amount": amount,
            "standingOrderRecurrence": standing_order_recurrence,
        }

        if destination_payee_account_uid:
            json_data["destinationPayeeAccountUid"] = destination_payee_account_uid
        if payment_recipient:
            json_data["paymentRecipient"] = payment_recipient
        if spending_category:
            json_data["spendingCategory"] = spending_category

        return self.client.put(
            f"/api/v2/payments/local/account/{account_uid}/category/{category_uid}/standing-orders",
            json_data=json_data,
        )

    def update_standing_order(
        self,
        account_uid: str,
        category_uid: str,
        payment_order_uid: str,
        reference: str,
        amount: Dict[str, Any],
        standing_order_recurrence: Dict[str, Any],
        spending_category: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update a standing order.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            payment_order_uid: Payment order UID
            reference: Payment reference
            amount: CurrencyAndAmount object
            standing_order_recurrence: StandingOrderRecurrence object
            spending_category: Spending category (optional)

        Requires: message signing and standing-order:create OAuth scope

        Returns:
            UpdateStandingOrderResponse object
        """
        json_data = {
            "paymentOrderUid": payment_order_uid,
            "reference": reference,
            "amount": amount,
            "standingOrderRecurrence": standing_order_recurrence,
        }

        if spending_category:
            json_data["spendingCategory"] = spending_category

        return self.client.put(
            f"/api/v2/payments/local/account/{account_uid}/category/{category_uid}/standing-orders/{payment_order_uid}",
            json_data=json_data,
        )

    def cancel_standing_order(
        self, account_uid: str, category_uid: str, payment_order_uid: str
    ) -> Dict[str, Any]:
        """
        Cancel a standing order.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            payment_order_uid: Payment order UID

        Requires: message signing and standing-order:delete OAuth scope

        Returns:
            Empty dict on success
        """
        return self.client.delete(
            f"/api/v2/payments/local/account/{account_uid}/category/{category_uid}/standing-orders/{payment_order_uid}"
        )

    def get_upcoming_payments(
        self, account_uid: str, category_uid: str, payment_order_uid: str, count: int = 10
    ) -> Dict[str, Any]:
        """
        List the next payment dates of a standing order.

        Args:
            account_uid: Account UID
            category_uid: Category UID
            payment_order_uid: Payment Order UID
            count: Number of next payment dates to retrieve (1-100, default: 10)

        Requires: standing-order:read OAuth scope

        Returns:
            NextPaymentDatesResponse object
        """
        params = {"count": count}
        return self.client.get(
            f"/api/v2/payments/local/account/{account_uid}/category/{category_uid}/standing-orders/{payment_order_uid}/upcoming-payments",
            params=params,
        )