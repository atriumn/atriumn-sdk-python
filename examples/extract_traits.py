#!/usr/bin/env python3
"""Example: Story trait extraction usage.

This example demonstrates how to use the Atriumn AI SDK to extract
traits from story text for identity analysis.
"""

from atriumn_ai import MCPClient


def main():
    """Main example function."""
    # Sample story text
    story_text = """
    Last summer, I decided to take on the challenge of learning rock climbing. 
    Despite my fear of heights, I was determined to push through my comfort zone. 
    I started with indoor climbing walls, methodically learning each technique. 
    When I finally attempted my first outdoor climb, I felt a mix of terror and 
    excitement. After three attempts, I successfully reached the top. The sense 
    of accomplishment was incredible, and I realized that persistence and careful 
    preparation can help overcome even deep-seated fears.
    """
    
    # Initialize client
    client = MCPClient()
    
    try:
        # Extract traits from the story
        print("=== Story Trait Extraction ===")
        print(f"Story: {story_text.strip()}")
        print()
        
        result = client.extract_traits_story(
            app="idynic",
            story_text=story_text
        )
        
        print("Extracted Traits:")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set your API key:")
        print("export ATRIUMN_API_KEY=your-api-key-here")
    
    finally:
        client.close()


if __name__ == "__main__":
    main()