#!/usr/bin/env python3
"""Example: Basic model recommendation usage.

This example demonstrates how to use the Atriumn AI SDK to get
model recommendations based on cost optimization.
"""

import os
from atriumn_ai import MCPClient


def main():
    """Main example function."""
    # Initialize client with API key from environment
    client = MCPClient()
    
    try:
        # Example 1: Get lowest cost model recommendation
        print("=== Cost-Optimized Model Recommendation ===")
        result = client.recommend_model(
            app="axiomiq",
            priority="lowest_cost",
            input_tokens=1000,
            output_tokens=500
        )
        print(f"Recommended model: {result}")
        print()
        
        # Example 2: Get fastest model recommendation
        print("=== Speed-Optimized Model Recommendation ===")
        result = client.recommend_model(
            app="axiomiq",
            priority="fastest",
            input_tokens=2000,
            output_tokens=1000
        )
        print(f"Recommended model: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set your API key:")
        print("export ATRIUMN_API_KEY=your-api-key-here")
    
    finally:
        client.close()


if __name__ == "__main__":
    main()