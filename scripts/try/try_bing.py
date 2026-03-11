import requests
import sys
from bs4 import BeautifulSoup

proxy = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}


def search_bing(query):
    url = f"https://www.bing.com/search?q={query}"

    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers, proxies=proxy)

    soup = BeautifulSoup(res.text, "html.parser")

    results = []

    for item in soup.select("li.b_algo h2 a"):
        results.append({"title": item.text, "url": item["href"]})

    return results[:5]


def extract_text_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, proxies=proxy, timeout=10)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        return f"Error fetching {url}: {e}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python try_bing.py <query>")
        sys.exit(1)

    query = sys.argv[1]
    search_results = search_bing(query)

    all_text = []
    for result in search_results:
        print(f"Fetching: {result['url']}")
        text = extract_text_from_url(result["url"])
        all_text.append(
            f"Source: {result['url']}\nTitle: {result['title']}\nContent: {text}\n"
            + "=" * 50
        )

    final_content = "\n\n".join(all_text)
    print("\n--- Concatenated Text Out ---")
    print(final_content[:2000] + "...")  # Print first 2000 chars to avoid flooding
