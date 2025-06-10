"""Core MCP Client for Atriumn AI SDK."""

import json
from typing import Any, Dict, Optional, Union

import httpx

from .config import Config
from .exceptions import APIError, AuthenticationError, TaskNotFoundError, ValidationError


class MCPClient:
    """Client for interacting with Atriumn MCP servers."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        **kwargs
    ):
        """Initialize the MCP Client."""
        self.config = Config(api_key=api_key, base_url=base_url, **kwargs)
        self.timeout = timeout
        self._client = httpx.Client(
            base_url=self.config.base_url,
            timeout=timeout,
            headers=self._get_headers(),
        )

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"atriumn-ai-sdk-python/{self.config.version}",
        }
        if self.config.api_key:
            headers["x-api-key"] = self.config.api_key
        return headers

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions."""
        if response.status_code == 401:
            raise AuthenticationError("Invalid API key or authentication failed")
        elif response.status_code == 404:
            raise TaskNotFoundError("Task not found")
        elif response.status_code == 422:
            raise ValidationError(f"Validation error: {response.text}")
        elif response.status_code >= 400:
            raise APIError(f"API error {response.status_code}: {response.text}")
        
        try:
            return response.json()
        except json.JSONDecodeError:
            raise APIError(f"Invalid JSON response: {response.text}")

    def run_task(
        self,
        task: str,
        app: str,
        input_data: Dict[str, Any],
        raw_response: bool = False,
    ) -> Union[Dict[str, Any], httpx.Response]:
        """Execute a task on the MCP server."""
        payload = {
            "task": task,
            "app": app,
            "input": input_data,
        }
        
        response = self._client.post("/tasks/execute", json=payload)
        
        if raw_response:
            return response
            
        return self._handle_response(response)

    def recommend_model(
        self,
        app: str,
        priority: str = "lowest_cost",
        input_tokens: int = 1000,
        output_tokens: int = 500,
        **kwargs
    ) -> Dict[str, Any]:
        """Convenience method for model recommendation."""
        input_data = {
            "priority": priority,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            **kwargs,
        }
        return self.run_task("recommend_model", app, input_data)

    def extract_traits_story(
        self,
        app: str,
        story_text: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Convenience method for extracting traits from a story."""
        input_data = {
            "story_text": story_text,
            **kwargs,
        }
        return self.run_task("extract_traits_story", app, input_data)

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()