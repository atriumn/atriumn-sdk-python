"""Tests for the MCP Client."""

import json
from unittest.mock import Mock, patch

import pytest
import httpx

from atriumn_ai.client import MCPClient
from atriumn_ai.exceptions import (
    APIError,
    AuthenticationError,
    TaskNotFoundError,
    ValidationError,
)


class TestMCPClient:
    """Test cases for MCPClient."""

    def setup_method(self):
        """Set up test fixtures."""
        self.api_key = "test-api-key"
        self.base_url = "https://api.test.com"
        self.client = MCPClient(api_key=self.api_key, base_url=self.base_url)

    def test_init(self):
        """Test client initialization."""
        assert self.client.config.api_key == self.api_key
        assert self.client.config.base_url == self.base_url
        assert self.client.timeout == 30.0

    def test_get_headers(self):
        """Test header generation."""
        headers = self.client._get_headers()
        assert headers["x-api-key"] == self.api_key
        assert headers["Content-Type"] == "application/json"
        assert "atriumn-ai-sdk-python" in headers["User-Agent"]

    @patch("httpx.Client.post")
    def test_run_task_success(self, mock_post):
        """Test successful task execution."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "result": {"data": "test"}}
        mock_post.return_value = mock_response

        result = self.client.run_task("test_task", "test_app", {"input": "data"})
        
        assert result["success"] is True
        assert result["result"]["data"] == "test"
        mock_post.assert_called_once()

    @patch("httpx.Client.post")
    def test_run_task_authentication_error(self, mock_post):
        """Test authentication error handling."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        with pytest.raises(AuthenticationError):
            self.client.run_task("test_task", "test_app", {"input": "data"})

    def test_recommend_model(self):
        """Test recommend_model convenience method."""
        with patch.object(self.client, 'run_task') as mock_run_task:
            mock_run_task.return_value = {"model": "gpt-4", "cost": 0.01}
            
            result = self.client.recommend_model(
                app="test_app",
                priority="lowest_cost",
                input_tokens=1000,
                output_tokens=500
            )
            
            mock_run_task.assert_called_once_with(
                "recommend_model",
                "test_app",
                {
                    "priority": "lowest_cost",
                    "input_tokens": 1000,
                    "output_tokens": 500,
                }
            )