# Atriumn AI SDK for Python

A minimal, production-ready Python SDK for the Atriumn AI orchestration service.

## Features

- **Async-only design** using `httpx.AsyncClient` for optimal performance
- **Single clean interface** with one public method: `run_task()`
- **Comprehensive error handling** with custom exception types
- **Type hints** and Pydantic validation for better developer experience
- **Environment variable support** for easy configuration
- **Context manager support** for proper resource cleanup

## Installation

```bash
pip install atriumn-sdk-ai-python
```

For development:
```bash
pip install atriumn-sdk-ai-python[dev]
```

## Quick Start

### Basic Usage

```python
import asyncio
from atriumn_sdk_ai import AtriumnClient

async def main():
    async with AtriumnClient(
        base_url="https://api.atriumn.com",
        api_key="your-api-key-here"
    ) as client:
        
        result = await client.run_task(
            app="idynic",
            task="extract_traits_story",
            input={
                "story": "I love solving complex problems and leading teams..."
            },
            options={
                "model": "gpt-4",
                "temperature": 0.7
            }
        )
        
        print(result)

asyncio.run(main())
```

### Environment Variables

Set environment variables to avoid hardcoding credentials:

```bash
export ATRIUMN_BASE_URL="https://api.atriumn.com"
export ATRIUMN_API_KEY="your-api-key-here"
```

Then use the client without parameters:

```python
async with AtriumnClient() as client:
    result = await client.run_task(
        app="axiomiq",
        task="analyze_job_requirements",
        input={"job_description": "Senior Python Developer..."}
    )
```

## API Reference

### AtriumnClient

#### Constructor

```python
AtriumnClient(
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: float = 60.0
)
```

**Parameters:**
- `base_url`: Base URL for the Atriumn AI service (or set `ATRIUMN_BASE_URL` env var)
- `api_key`: API key for authentication (or set `ATRIUMN_API_KEY` env var)
- `timeout`: Request timeout in seconds (default: 60.0)

#### Methods

##### `run_task()`

```python
async def run_task(
    app: str,
    task: str,
    input: Dict[str, Any],
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Execute an AI task through the Atriumn orchestration service.

**Parameters:**
- `app`: Application name (e.g., "idynic", "axiomiq")
- `task`: Task name to execute
- `input`: Input data for the task
- `options`: Optional task configuration (model settings, etc.)

**Returns:** Task execution result as a dictionary

**Raises:**
- `AtriumnAPIError`: If the API request fails
- `AtriumnAuthError`: If authentication fails  
- `AtriumnValidationError`: If request validation fails

##### `close()`

```python
async def close()
```

Manually close the HTTP client. Not needed when using context manager.

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from atriumn_sdk_ai import (
    AtriumnClient,
    AtriumnAPIError,
    AtriumnAuthError, 
    AtriumnValidationError
)

async with AtriumnClient() as client:
    try:
        result = await client.run_task(
            app="myapp",
            task="mytask", 
            input={"data": "test"}
        )
    except AtriumnAuthError:
        print("Authentication failed - check your API key")
    except AtriumnValidationError as e:
        print(f"Request validation failed: {e}")
    except AtriumnAPIError as e:
        print(f"API request failed: {e}")
```

## Examples

See the `examples/` directory for complete usage examples:

- `examples/run_task.py` - Basic usage patterns for different apps and tasks

## Development

### Setup

```bash
git clone https://github.com/atriumn/atriumn-sdk-ai-python
cd atriumn-sdk-ai-python
pip install -e .[dev]
```

### Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=atriumn_sdk_ai --cov-report=html
```

### Code Formatting

```bash
black .
ruff check .
```

## License

MIT License - see LICENSE file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/atriumn/atriumn-sdk-ai-python/issues)
- **Documentation**: [API Documentation](https://docs.atriumn.com)
- **Email**: support@atriumn.com