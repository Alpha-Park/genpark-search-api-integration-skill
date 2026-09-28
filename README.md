# GenPark Search Integration Skill

This repository contains the **GenPark Search Integration Skill** — an agent customization skill config (`skill.json`), a production-ready Python SDK client (`search_client.py`), and executable verification tests. It is designed to interface with the GenPark Search API to gather ranked search indexing content, extract citations, filter targets by domain names, and execute API connections using exponent backoffs.

---

## 🚀 Capabilities

* **Exponential Backoff Retries:** Automatically handles transient network issues and rate limiting by retrying failed endpoint calls with incremental delay.
* **Citation Resolution:** Groups resulting URLs into mapped numeric indices for easy integration inside LLM context window configurations.
* **API Filtering Rules:** Seamlessly limits searches to high-repute target domains.

---

## 🛠️ Setup & Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configuration:
   Set your API environment variables if executing requests against the live production server (otherwise, client executes in mock mode):
   * **PowerShell**:
     ```powershell
     $env:GENPARK_API_KEY="your_api_key"
     ```
   * **bash**:
     ```bash
     export GENPARK_API_KEY="your_api_key"
     ```

---

## 💻 SDK Usage Reference

```python
from search_client import GenParkSearchClient

# Initialize Client (mock mode by default)
client = GenParkSearchClient()

# Search
results = client.search(
    query="Zenith Speaker Reviews",
    max_results=3,
    filter_domain="techradar.com"
)

# Access results and citations
for item in results["ranked_results"]:
    print(f"[{item['citation_index']}] {item['title']}: {item['url']}")

print(results["citations"])
```

---

## 📜 License
This project is licensed under the MIT License.
