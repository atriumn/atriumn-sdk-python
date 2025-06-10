"""
Atriumn AI SDK

A minimal Python SDK for the Atriumn AI orchestration service.
"""

from .client import AtriumnClient
from .exceptions import (
    AtriumnError,
    AtriumnAPIError,
    AtriumnAuthError,
    AtriumnValidationError
)

__version__ = "0.1.0"

__all__ = [
    "AtriumnClient",
    "AtriumnError",
    "AtriumnAPIError", 
    "AtriumnAuthError",
    "AtriumnValidationError"
]