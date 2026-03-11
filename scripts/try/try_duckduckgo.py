import requests
import sys
import argparse
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

proxy = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}


def search_ddg(query, num_results=20):
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
        href = item["href"]
        # Handle protocol-relative URLs (e.g., //duckduckgo.com/...)
        if href.startswith("//"):
            href = "https:" + href

        # Extract the real URL from DDG's redirect (?uddg=...)
        if "duckduckgo.com/l/?uddg=" in href:
            parsed = urlparse(href)
            query_params = parse_qs(parsed.query)
            if "uddg" in query_params:
                href = query_params["uddg"][0]

        results.append({"title": item.text.strip(), "url": href})

    return results[:num_results]


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


def copy_to_clipboard(text):
    try:
        process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        process.communicate(text.encode("utf-8"))
        return True
    except Exception as e:
        print(f"Warning: Failed to copy to clipboard: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search DDG and extract content.")
    parser.add_argument("query", help="The search query")
    parser.add_argument(
        "-n", type=int, default=20, help="Number of results to fetch (default: 20)"
    )
    args = parser.parse_args()

    search_results = search_ddg(args.query, num_results=args.n)

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
    print(final_content)

    if copy_to_clipboard(final_content):
        print("\n✅ Success: All content has been copied to the clipboard.")
