"""
Atriumn AI SDK Client

Provides async interface to the Atriumn AI orchestration service.
"""
import os
from typing import Dict, Any, Optional

import httpx
from pydantic import BaseModel, Field

from .exceptions import AtriumnAPIError, AtriumnAuthError, AtriumnValidationError


class TaskRequest(BaseModel):
    """Request model for AI task execution."""
    app: str = Field(..., description="Application name (e.g., 'idynic', 'axiomiq')")
    task: str = Field(..., description="Task name to execute")
    input: Dict[str, Any] = Field(..., description="Input data for the task")
    options: Optional[Dict[str, Any]] = Field(None, description="Optional task configuration")


class AtriumnClient:
    """Async client for Atriumn AI orchestration service."""
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 60.0
    ):
        """
        Initialize the Atriumn client.
        
        Args:
            base_url: Base URL for the Atriumn AI service. Defaults to ATRIUMN_BASE_URL env var.
            api_key: API key for authentication. Defaults to ATRIUMN_API_KEY env var.
            timeout: Request timeout in seconds.
        """
        self.base_url = (base_url or os.getenv("ATRIUMN_BASE_URL", "")).rstrip('/')
        self.api_key = api_key or os.getenv("ATRIUMN_API_KEY")
        
        if not self.base_url:
            raise AtriumnValidationError("base_url is required. Set ATRIUMN_BASE_URL or pass base_url parameter.")
        
        if not self.api_key:
            raise AtriumnAuthError("api_key is required. Set ATRIUMN_API_KEY or pass api_key parameter.")
        
        self._client = httpx.AsyncClient(
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
    
    async def run_task(
        self,
        app: str,
        task: str,
        input: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute an AI task through the Atriumn orchestration service.
        
        Args:
            app: Application name (e.g., 'idynic', 'axiomiq')
            task: Task name to execute
            input: Input data for the task
            options: Optional task configuration
            
        Returns:
            Dict[str, Any]: Task execution result
            
        Raises:
            AtriumnAPIError: If the API request fails
            AtriumnAuthError: If authentication fails
            AtriumnValidationError: If request validation fails
        """
        request_data = TaskRequest(
            app=app,
            task=task,
            input=input,
            options=options
        )
        
        url = f"{self.base_url}/v1/prompt"
        
        try:
            response = await self._client.post(
                url,
                json=request_data.model_dump(exclude_none=True)
            )
            
            if response.status_code == 401:
                raise AtriumnAuthError("Authentication failed. Check your API key.")
            elif response.status_code == 400:
                error_detail = response.json().get("detail", "Validation error")
                raise AtriumnValidationError(f"Request validation failed: {error_detail}")
            elif response.status_code >= 400:
                error_detail = response.json().get("detail", "Unknown error")
                raise AtriumnAPIError(
                    f"API request failed with status {response.status_code}: {error_detail}"
                )
            
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPError as e:
            raise AtriumnAPIError(f"HTTP request failed: {str(e)}")
        except Exception as e:
            if isinstance(e, (AtriumnAPIError, AtriumnAuthError, AtriumnValidationError)):
                raise
            raise AtriumnAPIError(f"Unexpected error: {str(e)}")
    
    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()