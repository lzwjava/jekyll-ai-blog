import requests
import sys
import argparse
import subprocess
import os
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from readability import Document
from urllib.parse import urlparse, parse_qs

# Configuration
DEFAULT_PROXY = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
PROXY = {
    "http": os.environ.get("HTTP_PROXY", DEFAULT_PROXY["http"]),
    "https": os.environ.get("HTTPS_PROXY", DEFAULT_PROXY["https"]),
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
}


def search_google(query: str, num_results: int = 10) -> List[Dict[str, str]]:
    """Search Google by scraping web results directly."""
    url = f"https://www.google.com/search?q={query}&num={num_results}"

    try:
        response = requests.get(url, headers=HEADERS, proxies=PROXY, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error searching Google: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    # Google results are typically in div.g or div.tF2Cud
    # Anchors with h3 tags inside are usually the result links
    for g in soup.select(".g"):
        anchor = g.select_one("a")
        title_elem = g.select_one("h3")

        if anchor and title_elem:
            link = anchor["href"]
            title = title_elem.get_text()

            # Filter out internal google links
            if link.startswith("/search") or "google.com" in link and "/search" in link:
                continue

            results.append({"title": title, "url": link})

        if len(results) >= num_results:
            break

    return results


def extract_text_from_url(url):
    try:
        session = requests.Session()
        res = session.get(url, headers=HEADERS, proxies=PROXY, timeout=15)
        res.encoding = res.apparent_encoding

        if res.status_code != 200:
            return f"Error: Received status code {res.status_code}"

        soup = BeautifulSoup(res.text, "html.parser")

        # Remove irrelevant elements
        for element in soup(
            ["script", "style", "header", "footer", "nav", "aside", "form"]
        ):
            element.decompose()

        content_blocks = []

        # Site-specific selectors
        if "zhihu.com" in url:
            targets = soup.select(
                ".QuestionHeader-title, .RichContent-inner, .Post-RichTextContainer"
            )
        elif "zhidao.baidu.com" in url:
            targets = soup.select(
                ".wgt-best-mask, .wgt-best-content, .wgt-answers, .line.content, .best-text"
            )
        elif "wikipedia.org" in url:
            targets = soup.select("#firstHeading, .mw-parser-output p")
        elif "github.com" in url:
            targets = soup.select(".repository-content, article.markdown-body")
        else:
            # Generic extraction using readability-lxml
            try:
                doc = Document(res.text)
                summary_html = doc.summary()
                if summary_html:
                    summary_soup = BeautifulSoup(summary_html, "html.parser")
                    text = summary_soup.get_text(separator=" ", strip=True)
                    if len(text) > 100:  # Ensure it extracted meaningful content
                        return text
            except Exception as e:
                print(f"Readability failed for {url}: {e}")

            # Fallback to generic heuristics
            targets = soup.select("article, main, .main-content, #content, .content")
            if not targets:
                targets = [soup.find("body")]

        for t in targets:
            if t:
                text = t.get_text(separator=" ", strip=True)
                if text:
                    content_blocks.append(text)

        if content_blocks:
            return "\n\n".join(content_blocks)

        return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        return f"Error fetching {url}: {e}"


def format_llm_output(results):
    """Formats findings into a structured, LLM-friendly Markdown format."""
    blocks = []
    for i, res in enumerate(results):
        block = (
            f"### Source {i + 1}\n"
            f"**Title:** {res['title']}\n"
            f"**URL:** {res['url']}\n\n"
            f"**Content:**\n{res.get('content', 'No content extracted.')}\n"
            f"{'-' * 40}"
        )
        blocks.append(block)
    return "\n\n".join(blocks)


def copy_to_clipboard(text):
    try:
        process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        process.communicate(text.encode("utf-8"))
        return True
    except Exception:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Search & Extract for LLMs.")
    parser.add_argument("query", help="The search query")
    parser.add_argument(
        "-n", type=int, default=10, help="Number of results (default: 10)"
    )
    parser.add_argument("-o", "--output", help="Save output to file")
    args = parser.parse_args()

    print(f"Searching Google for: {args.query}")
    search_results = search_google(args.query, num_results=args.n)
    processed_results = []

    if not search_results:
        print("No results found.")
        sys.exit(0)

    print(f"Fetching {len(search_results)} results in parallel...")

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_info = {
            executor.submit(extract_text_from_url, r["url"]): r for r in search_results
        }

        for future in as_completed(future_to_info):
            info = future_to_info[future]
            try:
                content = future.result()
                processed_results.append({**info, "content": content})
                print(f"Done: {info['url']}")
            except Exception as e:
                print(f"Failed: {info['url']} ({e})")

    # Sort results to match original search order
    url_to_order = {res["url"]: i for i, res in enumerate(search_results)}
    processed_results.sort(key=lambda x: url_to_order.get(x["url"], 999))

    final_content = format_llm_output(processed_results)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"\n💾 Saved to: {args.output}")
    else:
        print("\n--- LLM Structured Output ---\n")
        print(final_content)

    if copy_to_clipboard(final_content):
        print("\n✅ Copied to clipboard.")
