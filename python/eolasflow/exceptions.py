"""EolasFlow SDK exceptions."""


class EolasFlowError(Exception):
    """Base exception for all EolasFlow SDK errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(message)


class AuthenticationError(EolasFlowError):
    """API key is invalid or missing."""
    pass


class RateLimitError(EolasFlowError):
    """Rate limit exceeded. Retry after the indicated time."""

    def __init__(self, message: str, retry_after: int = None, **kwargs):
        self.retry_after = retry_after
        super().__init__(message, **kwargs)


class NotFoundError(EolasFlowError):
    """Requested resource does not exist."""
    pass


class ValidationError(EolasFlowError):
    """Request data failed validation."""
    pass


class PlanLimitError(EolasFlowError):
    """Subscription plan limit exceeded."""
    pass
