import sys
import json
from search_client import GenParkSearchClient

def main():
    # Fix console encoding on Windows to prevent UnicodeErrors
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("=== GenPark Search Integration Agent Verification ===")
    
    # Initialize client in mock/simulation mode
    client = GenParkSearchClient()
    
    # Test Query A: Broad topic query
    query_a = "Zenith Smart Speaker reviews and specifications"
    print(f"\n[Scenario A] Executing Search: '{query_a}'")
    
    result_a = client.search(query=query_a, max_results=3)
    print("\nRanked Web Results:")
    for res in result_a["ranked_results"]:
        print(f"  [{res['citation_index']}] {res['title']}")
        print(f"      URL: {res['url']}")
        print(f"      Snippet: {res['snippet']}")
        
    print("\nStructured Citations Object:")
    print(json.dumps(result_a["citations"], indent=2))

    # Test Query B: Domain-restricted query
    query_b = "Zenith Audio"
    domain = "techradar.com"
    print(f"\n[Scenario B] Executing Search: '{query_b}' restricted to domain: '{domain}'")
    
    result_b = client.search(query=query_b, max_results=2, filter_domain=domain)
    print("\nFiltered Results:")
    for res in result_b["ranked_results"]:
        print(f"  [{res['citation_index']}] {res['title']}")
        print(f"      URL: {res['url']}")

if __name__ == "__main__":
    main()
