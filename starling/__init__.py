"""
Starling Bank Python SDK

A comprehensive Python wrapper for the Starling Bank API.
"""

from .client import StarlingClient
from .exceptions import (
    StarlingError,
    StarlingAPIError,
    StarlingAuthenticationError,
    StarlingNotFoundError,
    StarlingBadRequestError,
    StarlingForbiddenError,
    StarlingServerError,
)

__version__ = "0.1.0"

__all__ = [
    "StarlingClient",
    "StarlingError",
    "StarlingAPIError",
    "StarlingAuthenticationError",
    "StarlingNotFoundError",
    "StarlingBadRequestError",
    "StarlingForbiddenError",
    "StarlingServerError",
]