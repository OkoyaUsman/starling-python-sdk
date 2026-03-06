"""Main client for Starling Bank API."""

import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin
from .exceptions import (
    StarlingAPIError,
    StarlingAuthenticationError,
    StarlingForbiddenError,
    StarlingNotFoundError,
    StarlingBadRequestError,
    StarlingServerError,
)


class StarlingClient:
    """Main client for interacting with the Starling Bank API."""

    PRODUCTION_BASE_URL = "https://api.starlingbank.com"
    SANDBOX_BASE_URL = "https://api-sandbox.starlingbank.com"

    def __init__(
        self,
        access_token: str,
        sandbox: bool = False,
        user_agent: Optional[str] = None,
    ):
        """
        Initialize the Starling Bank client.

        Args:
            access_token: OAuth2 access token
            sandbox: Whether to use sandbox environment (default: False)
            user_agent: Custom User-Agent header (optional)
        """
        self.access_token = access_token
        self.base_url = (
            self.SANDBOX_BASE_URL if sandbox else self.PRODUCTION_BASE_URL
        )
        self.user_agent = user_agent or "starling-python-sdk/0.1.0"

        # Initialize API modules
        from . import accounts
        from . import account_holders
        from . import addresses
        from . import cards
        from . import direct_debits
        from . import feed
        from . import identity
        from . import payments
        from . import payees
        from . import savings_goals
        from . import settle_up
        from . import spaces

        self.accounts = accounts.AccountsAPI(self)
        self.account_holders = account_holders.AccountHoldersAPI(self)
        self.addresses = addresses.AddressesAPI(self)
        self.cards = cards.CardsAPI(self)
        self.direct_debits = direct_debits.DirectDebitsAPI(self)
        self.feed = feed.FeedAPI(self)
        self.identity = identity.IdentityAPI(self)
        self.payments = payments.PaymentsAPI(self)
        self.payees = payees.PayeesAPI(self)
        self.savings_goals = savings_goals.SavingsGoalsAPI(self)
        self.settle_up = settle_up.SettleUpAPI(self)
        self.spaces = spaces.SpacesAPI(self)

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None,
        stream: bool = False,
    ) -> requests.Response:
        """
        Make a request to the Starling Bank API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., '/api/v2/accounts')
            params: Query parameters
            json_data: JSON body for POST/PUT requests
            headers: Additional headers
            stream: Whether to stream the response

        Returns:
            Response object

        Raises:
            StarlingAPIError: For API errors
        """
        url = urljoin(self.base_url, endpoint)
        request_headers = {
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": self.user_agent,
            "Accept": "application/json",
        }

        if headers:
            request_headers.update(headers)

        # Only set Content-Type for JSON if not already set and we have JSON data
        if json_data and "Content-Type" not in request_headers:
            request_headers["Content-Type"] = "application/json"

        try:
            # Handle binary data separately
            if data is not None:
                response = requests.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    headers=request_headers,
                    stream=stream,
                )
            else:
                response = requests.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                    headers=request_headers,
                    stream=stream,
                )

            # Handle errors
            if response.status_code >= 400:
                self._handle_error(response)

            return response

        except requests.exceptions.RequestException as e:
            raise StarlingAPIError(f"Request failed: {str(e)}")

    def _handle_error(self, response: requests.Response):
        """Handle API errors."""
        status_code = response.status_code

        try:
            error_data = response.json()
            errors = error_data.get("errors", [])
            message = errors[0].get("message", "Unknown error") if errors else "Unknown error"
        except (ValueError, KeyError):
            message = response.text or f"HTTP {status_code}"

        if status_code == 401:
            raise StarlingAuthenticationError(message, status_code)
        elif status_code == 403:
            raise StarlingForbiddenError(message, status_code)
        elif status_code == 404:
            raise StarlingNotFoundError(message, status_code)
        elif status_code == 400:
            raise StarlingBadRequestError(message, status_code)
        elif status_code >= 500:
            raise StarlingServerError(message, status_code)
        else:
            raise StarlingAPIError(message, status_code)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make a GET request."""
        response = self._request("GET", endpoint, params=params, **kwargs)
        if response.status_code == 204:
            return {}
        return response.json()

    def post(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make a POST request."""
        response = self._request("POST", endpoint, json_data=json_data, **kwargs)
        if response.status_code == 204:
            return {}
        return response.json()

    def put(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make a PUT request."""
        response = self._request("PUT", endpoint, json_data=json_data, **kwargs)
        if response.status_code == 204:
            return {}
        return response.json()

    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a DELETE request."""
        response = self._request("DELETE", endpoint, **kwargs)
        if response.status_code == 204:
            return {}
        return response.json() if response.content else {}

    def get_stream(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Make a GET request with streaming."""
        return self._request("GET", endpoint, params=params, stream=True, **kwargs)