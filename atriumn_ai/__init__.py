"""Atriumn AI Python SDK.

A Python SDK for interacting with Atriumn MCP servers.
"""

from .client import MCPClient
from .config import Config
from .exceptions import (
    AtriumAIError,
    APIError,
    TaskNotFoundError,
    AuthenticationError,
    ValidationError,
)

__version__ = "0.1.0"
__all__ = [
    "MCPClient",
    "Config",
    "AtriumAIError",
    "APIError",
    "TaskNotFoundError",
    "AuthenticationError",
    "ValidationError",
]