"""Custom exceptions for Tradier API SDK."""

class TradierAPIError(Exception):
    """Base exception for Tradier API errors."""
    pass

class AuthenticationError(TradierAPIError):
    """Raised when authentication fails (e.g., invalid token)."""
    pass

class RateLimitError(TradierAPIError):
    """Raised when the API rate limit is exceeded."""
    pass
