# Atriumn AI Python SDK

A clean, minimal Python SDK for interacting with Atriumn MCP servers.

## Installation

```bash
pip install atriumn-ai-sdk
```

## Quick Start

```python
from atriumn_ai import MCPClient

# Initialize client
client = MCPClient(api_key="your-api-key")

# Get model recommendation
result = client.recommend_model(
    app="axiomiq",
    priority="lowest_cost",
    input_tokens=1000,
    output_tokens=500
)

# Extract traits from story
traits = client.extract_traits_story(
    app="idynic",
    story_text="Your story text here..."
)
```

## Features

- Simple API for task execution
- Authentication via API key
- App scoping (idynic, axiomiq, etc.)
- Type safety with Pydantic models
- Comprehensive error handling

## Environment Setup

```bash
export ATRIUMN_API_KEY="your-api-key-here"
```