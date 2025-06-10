"""Custom exceptions for the Atriumn AI SDK."""


class AtriumAIError(Exception):
    """Base exception class for Atriumn AI SDK."""
    pass


class APIError(AtriumAIError):
    """Exception raised for API-related errors."""
    pass


class AuthenticationError(AtriumAIError):
    """Exception raised for authentication failures."""
    pass


class TaskNotFoundError(AtriumAIError):
    """Exception raised when a requested task is not found."""
    pass


class ValidationError(AtriumAIError):
    """Exception raised for input validation errors."""
    pass