import os
import time
import urllib.parse
import requests
from typing import List, Dict, Any, Optional

class GenParkSearchError(Exception):
    """Custom exception raised when search client operations fail."""
    pass

class GenParkSearchClient:
    """
    Production-grade client for interfacing with GenPark Autopilot Search API.
    Handles dynamic payload construction, ranking logic, response sanitization,
    and automatic exponential backoff retries for robust server operation.
    """
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.genpark.ai/v1"):
        self.api_key = api_key or os.environ.get("GENPARK_API_KEY")
        self.base_url = base_url.rstrip("/")
        # Enable mock responses automatically if key is absent
        self.mock_mode = self.api_key is None or self.api_key == "mock"
        
        if self.mock_mode:
            print("[GenParkSearchClient] API key not found. Running in local simulation mode.")

    def search(self, query: str, max_results: int = 5, filter_domain: Optional[str] = None) -> Dict[str, Any]:
        """
        Queries the GenPark indexing service, resolves results, and generates structural citations.
        """
        if not query.strip():
            raise GenParkSearchError("Search query cannot be empty.")

        # If mock mode, construct realistic structured data locally
        if self.mock_mode:
            return self._simulate_search(query, max_results, filter_domain)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "GenPark-Agentic-SDK/1.0"
        }
        
        payload = {
            "query": query,
            "limit": max_results,
            "filter_domain": filter_domain
        }
        
        # Exponential backoff retry loop
        last_err = None
        for attempt in range(3):
            try:
                response = requests.post(
                    f"{self.base_url}/search", 
                    json=payload, 
                    headers=headers, 
                    timeout=15
                )
                response.raise_for_status()
                return self._parse_response(response.json())
            except Exception as e:
                last_err = e
                wait_time = 2 ** attempt
                print(f"[GenParkSearchClient] Warning: attempt {attempt+1} failed ({e}). Retrying in {wait_time}s...")
                time.sleep(wait_time)
                
        raise GenParkSearchError(f"GenPark API search failed after 3 attempts: {last_err}")

    def _parse_response(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses and structures the raw api response payload.
        """
        items = raw_data.get("results", [])
        ranked = []
        citations = {}
        
        for idx, item in enumerate(items):
            citation_id = idx + 1
            ranked.append({
                "title": item.get("title", "Untitled Source"),
                "url": item.get("url", ""),
                "snippet": item.get("snippet", ""),
                "citation_index": citation_id
            })
            citations[str(citation_id)] = item.get("url", "")
            
        return {
            "ranked_results": ranked,
            "citations": citations
        }

    def _simulate_search(self, query: str, max_results: int, filter_domain: Optional[str]) -> Dict[str, Any]:
        """
        Generates production-grade simulation data representing GenPark search indexing.
        """
        domain_str = filter_domain if filter_domain else "example.com"
        simulated_results = [
            {
                "title": f"Review of Zenith Smart Speaker on {domain_str}",
                "url": f"https://{domain_str}/reviews/zenith-speaker",
                "snippet": f"The Zenith speaker sets a high bar for agent-driven home hubs. The sound quality matches audiophile standards."
            },
            {
                "title": "Zenith AI Hardware Specifications",
                "url": "https://specs.zenith-audio.com/hub100",
                "snippet": "Technical specs sheet containing internal driver dimensioning, latency benchmarks, and pricing matrices."
            },
            {
                "title": "Top 10 Smart Hubs Comparison of 2026",
                "url": "https://gearcentral.org/best-speakers-2026",
                "snippet": "Zenith ranks #2 overall for its open APIs allowing custom automation scripts."
            }
        ]
        
        # Filter by domain if requested
        if filter_domain:
            simulated_results = [r for r in simulated_results if filter_domain in r["url"]]
            
        # Limit count
        simulated_results = simulated_results[:max_results]
        
        # Parse through standard parser to keep interface consistent
        return self._parse_response({"results": simulated_results})
