"""Custom exceptions for the Starling Bank SDK."""


class StarlingError(Exception):
    """Base exception for all Starling SDK errors."""

    pass


class StarlingAPIError(StarlingError):
    """Exception raised for API errors."""

    def __init__(self, message: str, status_code: int = None, errors: list = None):
        super().__init__(message)
        self.status_code = status_code
        self.errors = errors or []


class StarlingAuthenticationError(StarlingAPIError):
    """Exception raised for authentication errors (401)."""

    pass


class StarlingForbiddenError(StarlingAPIError):
    """Exception raised for forbidden errors (403)."""

    pass


class StarlingNotFoundError(StarlingAPIError):
    """Exception raised for not found errors (404)."""

    pass


class StarlingBadRequestError(StarlingAPIError):
    """Exception raised for bad request errors (400)."""

    pass


class StarlingServerError(StarlingAPIError):
    """Exception raised for server errors (5xx)."""

    pass