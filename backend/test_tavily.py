"""
Test script for Tavily global search integration
Run this to verify that Tavily is properly configured
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

def test_tavily_service():
    """Test the Tavily search service directly"""
    print("=" * 80)
    print("TEST 1: Tavily Search Service")
    print("=" * 80)
    
    try:
        from services.tavily_search_service import get_tavily_service
        
        service = get_tavily_service()
        
        if not service.client:
            print("[FAIL] Tavily client not initialized")
            print("       Check TAVILY_API_KEY in .env file")
            return False
        
        print("[OK] Tavily service initialized")
        
        # Test basic search
        print("\nPerforming test search: 'latest HR technology trends 2025'")
        result = service.search(
            query="latest HR technology trends 2025",
            search_depth="basic",
            max_results=3
        )
        
        if not result.get("success"):
            print(f"[FAIL] Search failed: {result.get('error', 'Unknown error')}")
            return False
        
        print(f"[OK] Search successful!")
        print(f"     Results: {len(result['results'])}")
        print(f"     Response time: {result.get('response_time', 0):.2f}s")
        
        # Display results
        print("\nSearch Results:")
        for i, item in enumerate(result['results'], 1):
            print(f"\n  [{i}] {item['title']}")
            print(f"      URL: {item['url']}")
            print(f"      Score: {item['score']:.2f}")
            print(f"      Preview: {item['content'][:100]}...")
        
        # Test formatted context
        print("\n" + "-" * 80)
        print("Testing formatted context...")
        context = service.search_context(
            query="what is employee net promoter score",
            search_depth="basic",
            max_results=2
        )
        
        print(f"[OK] Context generated ({len(context)} chars)")
        print("\nContext Preview:")
        print(context[:500] + "..." if len(context) > 500 else context)
        
        return True
        
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        print("       Make sure tavily-python is installed: pip install tavily-python")
        return False
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mcp_integration():
    """Test MCP server tools"""
    print("\n" + "=" * 80)
    print("TEST 2: MCP Server Integration")
    print("=" * 80)
    
    try:
        # Import mcp module
        import core.mcp as mcp_module
        
        # Check if tools exist
        tools_to_check = ["global_web_search", "search_for_context"]
        
        for tool_name in tools_to_check:
            if hasattr(mcp_module, tool_name):
                print(f"[OK] Tool '{tool_name}' found in MCP server")
            else:
                print(f"[WARN] Tool '{tool_name}' not found in MCP server")
                print(f"       Make sure to add the tool functions to core/mcp.py")
        
        return True
        
    except ImportError as e:
        print(f"[FAIL] Could not import MCP module: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Error checking MCP integration: {e}")
        return False


def test_environment():
    """Test environment configuration"""
    print("\n" + "=" * 80)
    print("TEST 3: Environment Configuration")
    print("=" * 80)
    
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Check required environment variables
    required_vars = {
        "TAVILY_API_KEY": "Tavily API key for web search",
    }
    
    all_present = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            masked = value[:10] + "..." if len(value) > 10 else value
            print(f"[OK] {var} = {masked}")
        else:
            print(f"[FAIL] {var} not found")
            print(f"       Description: {description}")
            all_present = False
    
    return all_present


def test_dependencies():
    """Test required dependencies"""
    print("\n" + "=" * 80)
    print("TEST 4: Dependencies")
    print("=" * 80)
    
    dependencies = [
        ("tavily", "tavily-python"),
        ("langchain", "langchain"),
        ("langchain_core", "langchain-core"),
        ("dotenv", "python-dotenv"),
    ]
    
    all_present = True
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"[OK] {package_name} installed")
        except ImportError:
            print(f"[FAIL] {package_name} not installed")
            print(f"       Install with: pip install {package_name}")
            all_present = False
    
    return all_present


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("TAVILY INTEGRATION TEST SUITE")
    print("=" * 80)
    
    results = {
        "Environment": test_environment(),
        "Dependencies": test_dependencies(),
        "Tavily Service": test_tavily_service(),
        "MCP Integration": test_mcp_integration(),
    }
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("Tavily integration is ready to use.")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Please fix the issues above before using Tavily search.")
    print("=" * 80)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())