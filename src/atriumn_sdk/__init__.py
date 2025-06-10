"""Atriumn SDK - Thin facade for Atriumn AI API."""

from .client import run_task
from .tasks import (
    extract_traits_story,
    extract_traits_document,
    tailor_resume,
    synthesize_identity,
    summarize_fit,
    recommend_model,
)

__version__ = "0.1.0"
__all__ = [
    "run_task",
    "extract_traits_story",
    "extract_traits_document", 
    "tailor_resume",
    "synthesize_identity",
    "summarize_fit",
    "recommend_model",
]