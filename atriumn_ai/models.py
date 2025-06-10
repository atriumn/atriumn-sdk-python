"""Data models for the Atriumn AI SDK."""

from typing import Any, Dict, List, Optional

try:
    from pydantic import BaseModel, Field
except ImportError:
    # Fallback for when pydantic is not available
    class BaseModel:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    def Field(**kwargs):
        return None


class TaskRequest(BaseModel):
    """Request model for task execution."""
    task: str = Field(..., description="Name of the task to execute")
    app: str = Field(..., description="Application scope")
    input: Dict[str, Any] = Field(..., description="Input data for the task")


class TaskResponse(BaseModel):
    """Response model for task execution."""
    success: bool = Field(..., description="Whether the task succeeded")
    result: Optional[Dict[str, Any]] = Field(None, description="Task result data")
    error: Optional[str] = Field(None, description="Error message if failed")
    execution_time: Optional[float] = Field(None, description="Execution time in seconds")


class ModelRecommendation(BaseModel):
    """Model recommendation response."""
    model_name: str = Field(..., description="Recommended model name")
    provider: str = Field(..., description="Model provider")
    estimated_cost: Optional[float] = Field(None, description="Estimated cost")
    reasoning: Optional[str] = Field(None, description="Recommendation reasoning")
    alternatives: Optional[List[Dict[str, Any]]] = Field(None, description="Alternative models")


class TraitExtraction(BaseModel):
    """Trait extraction response."""
    hard_traits: Dict[str, Any] = Field(..., description="Extracted hard traits")
    soft_traits: Dict[str, Any] = Field(..., description="Extracted soft traits")
    confidence_score: Optional[float] = Field(None, description="Overall confidence score")
    story_elements: Optional[Dict[str, Any]] = Field(None, description="Analyzed story elements")