import asyncio
import sys
import os
from pathlib import Path

# Add backend to path to ensure imports work
sys.path.append(str(Path(__file__).parent))

from services.chat_pipeline import get_chat_pipeline

async def test_pipeline_web_search():
    print("="*60)
    print("TEST: Chat Pipeline Web Search Integration")
    print("="*60)

    try:
        print("[1] Initializing Chat Pipeline...")
        pipeline = get_chat_pipeline()
        print("[OK] Pipeline initialized")

        # Test Query that should trigger web search
        query = "What are the latest HR technology trends for 2025?"
        print(f"\n[2] Running pipeline with query: '{query}'")
        
        # Run the pipeline
        response = await pipeline.run(query)
        
        print("\n[3] Pipeline Response:")
        print("-" * 50)
        print(response)
        print("-" * 50)
        
        # Basic validation
        if response and "I couldn't process" not in response:
            print("\n[SUCCESS] Pipeline returned a valid response.")
        else:
            print("\n[FAIL] Pipeline returned error or fallback response.")

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_pipeline_web_search())
