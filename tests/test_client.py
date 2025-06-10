"""
Tests for the Atriumn AI SDK Client
"""
import pytest
import httpx
from unittest.mock import AsyncMock, patch

from atriumn_sdk_ai import AtriumnClient
from atriumn_sdk_ai.exceptions import (
    AtriumnAPIError,
    AtriumnAuthError,
    AtriumnValidationError
)


@pytest.fixture
def client():
    """Create a test client instance."""
    return AtriumnClient(
        base_url="https://api.test.atriumn.com",
        api_key="test-api-key"
    )


@pytest.fixture
def mock_response():
    """Create a mock HTTP response."""
    response = AsyncMock(spec=httpx.Response)
    response.status_code = 200
    response.json.return_value = {
        "result": "Task completed successfully",
        "data": {"output": "test output"}
    }
    return response


class TestAtriumnClient:
    """Test cases for AtriumnClient."""
    
    def test_client_initialization(self):
        """Test client initialization with parameters."""
        client = AtriumnClient(
            base_url="https://api.test.atriumn.com",
            api_key="test-key"
        )
        assert client.base_url == "https://api.test.atriumn.com"
        assert client.api_key == "test-key"
    
    def test_client_initialization_from_env(self):
        """Test client initialization from environment variables."""
        with patch.dict('os.environ', {
            'ATRIUMN_BASE_URL': 'https://env.test.com',
            'ATRIUMN_API_KEY': 'env-key'
        }):
            client = AtriumnClient()
            assert client.base_url == "https://env.test.com"
            assert client.api_key == "env-key"
    
    def test_client_missing_base_url(self):
        """Test client raises error when base_url is missing."""
        with pytest.raises(AtriumnValidationError, match="base_url is required"):
            AtriumnClient(api_key="test-key")
    
    def test_client_missing_api_key(self):
        """Test client raises error when api_key is missing."""
        with pytest.raises(AtriumnAuthError, match="api_key is required"):
            AtriumnClient(base_url="https://test.com")
    
    @pytest.mark.asyncio
    async def test_run_task_success(self, client, mock_response):
        """Test successful task execution."""
        with patch.object(client._client, 'post', return_value=mock_response):
            result = await client.run_task(
                app="idynic",
                task="extract_traits",
                input={"text": "test document"},
                options={"model": "gpt-4"}
            )
            
            assert result == {
                "result": "Task completed successfully",
                "data": {"output": "test output"}
            }
            
            # Verify the request was made correctly
            client._client.post.assert_called_once_with(
                "https://api.test.atriumn.com/v1/prompt",
                json={
                    "app": "idynic",
                    "task": "extract_traits",
                    "input": {"text": "test document"},
                    "options": {"model": "gpt-4"}
                }
            )
    
    @pytest.mark.asyncio
    async def test_run_task_without_options(self, client, mock_response):
        """Test task execution without options."""
        with patch.object(client._client, 'post', return_value=mock_response):
            await client.run_task(
                app="axiomiq",
                task="analyze_data",
                input={"data": [1, 2, 3]}
            )
            
            # Verify options was excluded from the request
            client._client.post.assert_called_once_with(
                "https://api.test.atriumn.com/v1/prompt",
                json={
                    "app": "axiomiq",
                    "task": "analyze_data",
                    "input": {"data": [1, 2, 3]}
                }
            )
    
    @pytest.mark.asyncio
    async def test_run_task_auth_error(self, client):
        """Test authentication error handling."""
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = 401
        mock_response.json.return_value = {"detail": "Invalid API key"}
        
        with patch.object(client._client, 'post', return_value=mock_response):
            with pytest.raises(AtriumnAuthError, match="Authentication failed"):
                await client.run_task(
                    app="test",
                    task="test",
                    input={}
                )
    
    @pytest.mark.asyncio
    async def test_run_task_validation_error(self, client):
        """Test validation error handling."""
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = 400
        mock_response.json.return_value = {"detail": "Invalid task name"}
        
        with patch.object(client._client, 'post', return_value=mock_response):
            with pytest.raises(AtriumnValidationError, match="Request validation failed"):
                await client.run_task(
                    app="test",
                    task="invalid_task",
                    input={}
                )
    
    @pytest.mark.asyncio
    async def test_run_task_api_error(self, client):
        """Test general API error handling."""
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = 500
        mock_response.json.return_value = {"detail": "Internal server error"}
        
        with patch.object(client._client, 'post', return_value=mock_response):
            with pytest.raises(AtriumnAPIError, match="API request failed with status 500"):
                await client.run_task(
                    app="test",
                    task="test",
                    input={}
                )
    
    @pytest.mark.asyncio
    async def test_run_task_http_error(self, client):
        """Test HTTP error handling."""
        with patch.object(client._client, 'post', side_effect=httpx.HTTPError("Connection failed")):
            with pytest.raises(AtriumnAPIError, match="HTTP request failed"):
                await client.run_task(
                    app="test",
                    task="test",
                    input={}
                )
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager usage."""
        async with AtriumnClient(
            base_url="https://test.com",
            api_key="test-key"
        ) as client:
            assert isinstance(client, AtriumnClient)
        
        # Client should be closed after exiting context
        assert client._client.is_closed
    
    @pytest.mark.asyncio
    async def test_close_method(self, client):
        """Test explicit close method."""
        await client.close()
        assert client._client.is_closed