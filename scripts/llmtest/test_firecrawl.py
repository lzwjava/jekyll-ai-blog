import os
import requests

url = "https://api.firecrawl.dev/v2/scrape"

payload = {
    "url": "lzwjava.github.io",
    "onlyMainContent": True,
    "maxAge": 172800000,
    "parsers": ["pdf"],
    "formats": ["markdown"],
}

headers = {
    "Authorization": f"Bearer {os.getenv('FIRECRAWL_API_KEY')}",
    "Content-Type": "application/json",
}

response = requests.post(url, json=payload, headers=headers, timeout=30)
print(response.json())
