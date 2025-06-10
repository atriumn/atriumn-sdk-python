#!/usr/bin/env python3
"""
Example usage of the Atriumn AI SDK

This example demonstrates how to use the AtriumnClient to execute AI tasks
through the Atriumn orchestration service.
"""
import asyncio
import os
from atriumn_sdk_ai import AtriumnClient


async def main():
    """Main example function."""
    
    # Initialize the client
    # You can pass base_url and api_key directly, or set them as environment variables:
    # export ATRIUMN_BASE_URL="https://api.atriumn.com"
    # export ATRIUMN_API_KEY="your-api-key-here"
    
    async with AtriumnClient(
        base_url=os.getenv("ATRIUMN_BASE_URL", "https://api.atriumn.com"),
        api_key=os.getenv("ATRIUMN_API_KEY", "your-api-key-here")
    ) as client:
        
        # Example 1: Extract traits from a story (Idynic app)
        print("Example 1: Extracting traits from a story...")
        try:
            result = await client.run_task(
                app="idynic",
                task="extract_traits_story",
                input={
                    "story": "I love solving complex problems and leading teams through challenging projects. "
                            "Last year, I successfully launched a new product feature that increased user engagement by 40%."
                },
                options={
                    "model": "gpt-4",
                    "temperature": 0.7
                }
            )
            print(f"✅ Success: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*50 + "\n")
        
        # Example 2: Analyze job requirements (Axiomiq app)
        print("Example 2: Analyzing job requirements...")
        try:
            result = await client.run_task(
                app="axiomiq",
                task="analyze_job_requirements",
                input={
                    "job_description": "We're looking for a Senior Software Engineer with 5+ years of Python experience, "
                                     "strong knowledge of machine learning, and leadership skills.",
                    "company_info": {
                        "name": "TechCorp Inc.",
                        "industry": "AI/ML"
                    }
                }
            )
            print(f"✅ Success: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*50 + "\n")
        
        # Example 3: Simple task without options
        print("Example 3: Simple task execution...")
        try:
            result = await client.run_task(
                app="general",
                task="summarize_text",
                input={
                    "text": "The Atriumn AI orchestration service provides a unified interface for running "
                           "various AI tasks across different applications. It supports multiple models and "
                           "provides consistent error handling and response formatting."
                }
            )
            print(f"✅ Success: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())