"""Configuration management for Atriumn AI SDK."""

import os
from typing import Optional


class Config:
    """Configuration class for the Atriumn AI SDK."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        version: str = "0.1.0",
        **kwargs
    ):
        """Initialize configuration."""
        self.api_key = api_key or self._load_api_key()
        self.base_url = base_url or self._load_base_url()
        self.version = version
        
        # Additional configuration
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _load_api_key(self) -> Optional[str]:
        """Load API key from environment variables."""
        return (
            os.getenv("ATRIUMN_API_KEY") or
            os.getenv("ATRIUMN_AI_API_KEY") or
            os.getenv("API_KEY")
        )

    def _load_base_url(self) -> str:
        """Load base URL from environment variables or use default."""
        return (
            os.getenv("ATRIUMN_API_URL") or
            os.getenv("ATRIUMN_BASE_URL") or
            "https://api.atriumn.ai"
        )