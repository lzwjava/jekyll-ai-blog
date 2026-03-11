---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enterprise Web Search Workarounds
translated: false
type: note
---

Question: How can a simple web search system be implemented in a banking enterprise environment where external APIs like Tavily are not allowed, but browsers (Google/Edge/Chrome) are allowed and Python requests can access the internet through a corporate proxy?

Answer:

In many **banking or highly regulated enterprise environments**, direct use of external search APIs (such as Tavily, SerpAPI, or other AI search tools) is often blocked due to **security, compliance, and data leakage risks**. However, these environments typically still allow:

* Normal web browsing through **corporate proxies**
* Access to search engines such as Ecosia, Google or Bing
* Programmatic HTTP requests through approved proxy servers

Therefore, a simple web search system can be implemented using **three practical approaches**.

---

## 1. Browser Automation (Most Similar to Copilot Behavior)

This approach uses a **real browser controlled by code** to perform searches just like a human user.

### Architecture

```
User Query
    ↓
Python Service
    ↓
Playwright / Selenium
    ↓
Corporate Proxy
    ↓
Google / Bing
    ↓
Parse Result Page
    ↓
Return Titles + Links + Snippets
```

### Why This Works in Enterprises

* Uses **normal browser traffic**
* Appears identical to employee browsing
* Works even when many APIs are blocked

### Example Using Playwright (Python)

```python
from playwright.sync_api import sync_playwright

def search_google(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"https://www.google.com/search?q={query}")

        results = page.query_selector_all("h3")

        output = []
        for r in results[:5]:
            output.append(r.inner_text())

        browser.close()
        return output

print(search_google("latest fed interest rate"))
```

### Advantages

* Works behind corporate proxy
* Harder for search engines to block
* Very reliable

### Disadvantages

* Requires installing browser automation tools
* Slightly slower than API calls

---

# 2. Direct HTTP Search (Lightweight Python Requests)

If the proxy allows HTTP requests, you can **query search engine HTML directly** and parse results.

### Architecture

```
Query
 ↓
Python requests
 ↓
Corporate Proxy
 ↓
Search Engine HTML
 ↓
HTML Parser (BeautifulSoup)
 ↓
Results
```

### Example

```python
import requests
from bs4 import BeautifulSoup

proxy = {
    "http": "http://proxy.company.com:8080",
    "https": "http://proxy.company.com:8080"
}

def search_bing(query):
    url = f"https://www.bing.com/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers, proxies=proxy)

    soup = BeautifulSoup(res.text, "html.parser")

    results = []

    for item in soup.select("li.b_algo h2 a"):
        results.append({
            "title": item.text,
            "url": item["href"]
        })

    return results[:5]

print(search_bing("US inflation rate 2026"))
```

### Advantages

* Very simple
* Fast
* Easy to integrate with LLM tools

### Disadvantages

* Search engines may rate-limit
* HTML structure may change

---

# 3. Internal Search Proxy Service (Best Enterprise Architecture)

Large companies often create a **central internal web search gateway**.

Instead of every tool accessing the internet, they call an **internal service**.

### Architecture

```
LLM / Copilot
      ↓
Internal Search API
      ↓
Enterprise Proxy
      ↓
Google / Bing
      ↓
Content Parser
      ↓
Clean JSON Results
```

Example API response:

```json
{
  "query": "Fed interest rate",
  "results": [
    {
      "title": "Federal Reserve Interest Rate Decision",
      "url": "https://www.federalreserve.gov",
      "snippet": "The Federal Reserve maintained..."
    }
  ]
}
```

### Benefits

* Security team can audit requests
* Prevents data leaks
* Caches results
* Can filter banned websites

This is **very similar to how enterprise Copilot tools work**.

---

# 4. Combine With LLM Retrieval Pipeline

Once search results are obtained, the system can fetch the content.

Pipeline example:

```
User Question
   ↓
Search Engine Query
   ↓
Top 5 URLs
   ↓
Fetch HTML
   ↓
Extract Text
   ↓
Chunk Content
   ↓
Send to LLM
   ↓
Final Answer
```

Python example for fetching article text:

```python
import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    paragraphs = soup.find_all("p")

    text = "\n".join(p.text for p in paragraphs)

    return text[:5000]
```

---

# 5. Why Microsoft Copilot Works in Enterprises

Enterprise Copilot systems typically use:

1. **Bing internal APIs**
2. **Corporate proxy routing**
3. **Content filtering**
4. **Enterprise security layers**

So the architecture is roughly:

```
Copilot
  ↓
Microsoft Bing API
  ↓
Safe Search Filter
  ↓
Enterprise Security Gateway
  ↓
Internet
```

Your internal system can replicate **80% of this functionality** with:

* Search scraping
* Proxy usage
* Content extraction
* LLM summarization

---

# 6. Best Minimal Enterprise Setup

For a **bank environment**, a simple architecture would be:

```
Python Search Service
    │
    ├── requests + proxy
    │
    ├── Ecosia/Bing/Google HTML parsing
    │
    ├── Fetch top 3 pages
    │
    └── Return text to LLM
```

Tech stack:

* Python
* requests
* BeautifulSoup
* corporate proxy
* optional Playwright

This can be built in **~200 lines of code**.

---

# 7. Key Enterprise Considerations

### Security

* Prevent query logging of sensitive data
* Sanitize user inputs

### Compliance

* Whitelist domains
* Block risky sites

### Performance

* Cache search results
* Limit page fetch size

### Stability

* Use multiple search engines (Bing + DuckDuckGo)

---

# 8. Simple Enterprise Search Pipeline Example

```
User Question
     ↓
Search Engine Query
     ↓
Top 5 Results
     ↓
Download Pages
     ↓
Extract Text
     ↓
LLM Summarization
     ↓
Answer + Citations
```

This is essentially **how modern AI search agents work**.

---

If helpful, I can also show:

* **A complete 150-line Python enterprise search agent**
* **How to build a Copilot-like web search tool**
* **How OpenAI / Perplexity style search pipelines work internally**

References:

* [https://playwright.dev/python/docs/intro](https://playwright.dev/python/docs/intro)
* [https://www.selenium.dev/documentation/](https://www.selenium.dev/documentation/)
* [https://requests.readthedocs.io/en/latest/](https://requests.readthedocs.io/en/latest/)
* [https://www.crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)