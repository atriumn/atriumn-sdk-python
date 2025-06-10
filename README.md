# Atriumn SDK

Thin facade SDK for Atriumn AI API.

## Installation

```bash
pip install atriumn-sdk
```

## Usage

```python
import asyncio
from atriumn_sdk import extract_traits_story, recommend_model

async def main():
    # Extract traits from a story
    result = await extract_traits_story(
        input={"story_text": "Your story here..."},
        app="idynic",
        base_url="https://api.atriumn.ai",
        api_key="your-api-key"
    )
    
    # Get model recommendation
    model = await recommend_model(
        input={"priority": "lowest_cost", "input_tokens": 1000},
        app="axiomiq", 
        base_url="https://api.atriumn.ai",
        api_key="your-api-key"
    )

asyncio.run(main())
```

## Available Tasks

- `extract_traits_story`
- `extract_traits_document`
- `tailor_resume`
- `synthesize_identity`
- `summarize_fit`
- `recommend_model`

All tasks are async functions that take `input`, `app`, `base_url`, and `api_key` parameters.