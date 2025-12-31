import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Check if tavily is available
try:
    from tavily import TavilyClient
    HAS_TAVILY = True
except ImportError:
    HAS_TAVILY = False
    TavilyClient = None
    logger.warning("Tavily SDK not installed. Run: pip install tavily-python")


class TavilySearchService:
    """Service for performing global web searches using Tavily API"""
    
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.client = None
        
        if not self.api_key:
            logger.warning("TAVILY_API_KEY not found in environment variables")
            return
            
        if not HAS_TAVILY:
            logger.warning("Tavily SDK not available")
            return
            
        try:
            self.client = TavilyClient(api_key=self.api_key)
            logger.info("Tavily search service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Tavily client: {e}")
    
    def search(
        self,
        query: str,
        search_depth: str = "basic",
        max_results: int = 5,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Perform a web search using Tavily API
        
        Args:
            query: Search query string
            search_depth: "basic" or "advanced" (advanced costs more but is more thorough)
            max_results: Maximum number of results to return (1-10)
            include_domains: List of domains to include in search
            exclude_domains: List of domains to exclude from search
            
        Returns:
            Dict containing search results and metadata
        """
        if not self.client:
            return {
                "success": False,
                "error": "Tavily search service not available",
                "results": []
            }
        
        try:
            # Validate max_results
            max_results = max(1, min(10, max_results))
            
            # Prepare search parameters
            search_params = {
                "query": query,
                "search_depth": search_depth,
                "max_results": max_results
            }
            
            if include_domains:
                search_params["include_domains"] = include_domains
            
            if exclude_domains:
                search_params["exclude_domains"] = exclude_domains
            
            logger.info(f"Performing Tavily search: query='{query}', depth={search_depth}, max={max_results}")
            
            # Perform search
            response = self.client.search(**search_params)
            
            # Extract and format results
            results = []
            if response and "results" in response:
                for item in response["results"]:
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "content": item.get("content", ""),
                        "score": item.get("score", 0.0),
                        "published_date": item.get("published_date", "")
                    })
            
            logger.info(f"Tavily search returned {len(results)} results")
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "total_results": len(results),
                "answer": response.get("answer", ""),  # Tavily may provide a direct answer
                "images": response.get("images", []),
                "response_time": response.get("response_time", 0)
            }
            
        except Exception as e:
            logger.error(f"Tavily search failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": []
            }
    
    def search_context(
        self,
        query: str,
        search_depth: str = "advanced",
        max_results: int = 5
    ) -> str:
        """
        Perform a search and return formatted context for LLM consumption
        
        Args:
            query: Search query string
            search_depth: "basic" or "advanced"
            max_results: Maximum number of results
            
        Returns:
            Formatted string with search results as context
        """
        search_result = self.search(query, search_depth, max_results)
        
        if not search_result["success"]:
            return f"Search failed: {search_result.get('error', 'Unknown error')}"
        
        # Format results as context
        context_parts = [f"Search results for: {query}\n"]
        
        # Add direct answer if available
        if search_result.get("answer"):
            context_parts.append(f"Direct Answer: {search_result['answer']}\n")
        
        # Add search results
        for i, result in enumerate(search_result["results"], 1):
            context_parts.append(
                f"\n[{i}] {result['title']}\n"
                f"URL: {result['url']}\n"
                f"Content: {result['content']}\n"
                f"Relevance Score: {result['score']:.2f}"
            )
            
            if result.get("published_date"):
                context_parts.append(f"Published: {result['published_date']}")
            
            context_parts.append("")  # Empty line between results
        
        return "\n".join(context_parts)


# Singleton instance
_tavily_service = None

def get_tavily_service() -> TavilySearchService:
    """Get or create the Tavily search service singleton"""
    global _tavily_service
    if _tavily_service is None:
        _tavily_service = TavilySearchService()
    return _tavily_service