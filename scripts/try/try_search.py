import requests
import sys
from bs4 import BeautifulSoup

proxy = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}


def search_ddg(query):
    # Using DuckDuckGo's html version which is easier to scrape
    url = f"https://html.duckduckgo.com/html/?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://duckduckgo.com/",
    }

    res = requests.get(url, headers=headers, proxies=proxy)
    if res.status_code != 200:
        print(f"Error searching DDG: {res.status_code}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    # DDG HTML version uses .result__title and .result__a
    for item in soup.select(".result__title .result__a"):
        results.append({"title": item.text.strip(), "url": item["href"]})

    return results[:5]


def extract_text_from_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://www.bing.com/",
        }
        session = requests.Session()
        res = session.get(url, headers=headers, proxies=proxy, timeout=15)
        res.encoding = res.apparent_encoding

        if res.status_code != 200:
            return f"Error: Received status code {res.status_code}"

        soup = BeautifulSoup(res.text, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.decompose()

        # Try to find main content or fallback to body
        content_blocks = []

        # Site-specific selectors
        if "zhihu.com" in url:
            # Zhihu specific targets
            targets = soup.select(
                ".QuestionHeader-title, .RichContent-inner, .Post-RichTextContainer"
            )
            for t in targets:
                content_blocks.append(t.get_text(separator=" ", strip=True))
        elif "zhidao.baidu.com" in url:
            targets = soup.select(
                ".wgt-best-mask, .wgt-best-content, .wgt-answers, .line.content, .best-text"
            )
            for t in targets:
                content_blocks.append(t.get_text(separator=" ", strip=True))

        if content_blocks:
            return "\n".join(content_blocks)

        # Fallback for other sites or if specific selectors failed
        return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        return f"Error fetching {url}: {e}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python try_bing.py <query>")
        sys.exit(1)

    query = sys.argv[1]
    search_results = search_ddg(query)

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
