from services.tavily_search_service import get_tavily_service

# Test basic search
service = get_tavily_service()
result = service.search("latest HR technology trends 2025", max_results=3)

print(f"Success: {result['success']}")
print(f"Results: {len(result['results'])}")

for i, r in enumerate(result['results'], 1):
    print(f"\n{i}. {r['title']}")
    print(f"   URL: {r['url']}")
    print(f"   Score: {r['score']}")