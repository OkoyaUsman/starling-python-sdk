"""Cards API endpoints."""

from typing import Optional, Dict, Any


class CardsAPI:
    """API for card-related operations."""

    def __init__(self, client):
        """Initialize with a StarlingClient instance."""
        self.client = client

    def get_cards(self) -> Dict[str, Any]:
        """
        Get all the cards for an account holder.

        Requires: card:read OAuth scope

        Returns:
            Cards object containing list of cards
        """
        return self.client.get("/api/v2/cards")

    def update_card_lock(self, card_uid: str, enabled: bool) -> Dict[str, Any]:
        """
        Update card lock.

        Args:
            card_uid: Card UID
            enabled: Whether the card should be unlocked (True) or locked (False)

        Requires: card-control:edit OAuth scope

        Returns:
            Empty dict on success
        """
        json_data = {"enabled": enabled}
        return self.client.put(f"/api/v2/cards/{card_uid}/controls/enabled", json_data=json_data)

    def update_atm_enabled(self, card_uid: str, enabled: bool) -> Dict[str, Any]:
        """
        Update ATM withdrawal control.

        Args:
            card_uid: Card UID
            enabled: Whether ATM withdrawals should be allowed

        Requires: card-control:edit OAuth scope

        Returns:
            Empty dict on success
        """
        json_data = {"enabled": enabled}
        return self.client.put(f"/api/v2/cards/{card_uid}/controls/atm-enabled", json_data=json_data)

    def update_online_enabled(self, card_uid: str, enabled: bool) -> Dict[str, Any]:
        """
        Update online payments control.

        Args:
            card_uid: Card UID
            enabled: Whether online payments should be allowed

        Requires: card-control:edit OAuth scope

        Returns:
            Empty dict on success
        """
        json_data = {"enabled": enabled}
        return self.client.put(f"/api/v2/cards/{card_uid}/controls/online-enabled", json_data=json_data)

    def update_pos_enabled(self, card_uid: str, enabled: bool) -> Dict[str, Any]:
        """
        Update card present payments (contactless and chip and pin) control.

        Args:
            card_uid: Card UID
            enabled: Whether card present payments should be allowed

        Requires: card-control:edit OAuth scope

        Returns:
            Empty dict on success
        """
        json_data = {"enabled": enabled}
        return self.client.put(f"/api/v2/cards/{card_uid}/controls/pos-enabled", json_data=json_data)

    def update_mobile_wallet_enabled(self, card_uid: str, enabled: bool) -> Dict[str, Any]:
        """
        Update mobile wallet payments control.

        Args:
            card_uid: Card UID
            enabled: Whether mobile wallet payments should be allowed

        Requires: card-control:edit OAuth scope

        Returns:
            Empty dict on success
        """
        json_data = {"enabled": enabled}
        return self.client.put(
            f"/api/v2/cards/{card_uid}/controls/mobile-wallet-enabled", json_data=json_data
        )

    def update_gambling_enabled(self, card_uid: str, enabled: bool) -> Dict[str, Any]:
        """
        Update gambling payments control.

        Args:
            card_uid: Card UID
            enabled: Whether gambling payments should be allowed

        Requires: card-control:edit OAuth scope

        Returns:
            Empty dict on success
        """
        json_data = {"enabled": enabled}
        return self.client.put(f"/api/v2/cards/{card_uid}/controls/gambling-enabled", json_data=json_data)

    def update_mag_stripe_enabled(self, card_uid: str, enabled: bool) -> Dict[str, Any]:
        """
        Update magstripe payments control.

        Args:
            card_uid: Card UID
            enabled: Whether magstripe payments should be allowed

        Requires: card-control:edit OAuth scope

        Returns:
            Empty dict on success
        """
        json_data = {"enabled": enabled}
        return self.client.put(f"/api/v2/cards/{card_uid}/controls/mag-stripe-enabled", json_data=json_data)

    def update_currency_switch(self, card_uid: str, enabled: bool, currency: str) -> Dict[str, Any]:
        """
        Update currency switch payments control.

        Args:
            card_uid: Card UID
            enabled: Whether currency switch payments should be allowed
            currency: Currency code (e.g., 'GBP', 'EUR')

        Requires: card-control:edit OAuth scope

        Returns:
            Empty dict on success
        """
        json_data = {"enabled": enabled, "currency": currency}
        return self.client.put(f"/api/v2/cards/{card_uid}/controls/currency-switch", json_data=json_data)