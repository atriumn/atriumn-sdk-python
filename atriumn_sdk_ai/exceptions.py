"""
Atriumn SDK Exceptions

Custom exception classes for the Atriumn AI SDK.
"""


class AtriumnError(Exception):
    """Base exception for all Atriumn SDK errors."""
    pass


class AtriumnAPIError(AtriumnError):
    """Raised when API requests fail."""
    pass


class AtriumnAuthError(AtriumnError):
    """Raised when authentication fails."""
    pass


class AtriumnValidationError(AtriumnError):
    """Raised when request validation fails."""
    pass