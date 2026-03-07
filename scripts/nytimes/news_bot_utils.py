import requests
from bs4 import BeautifulSoup
import os
import re
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")


def fetch_html_content(url):
    try:
        print(f"Fetching HTML content from: {url}")
        response = requests.get(url, timeout=15, verify=False)
        response.raise_for_status()
        print(f"Successfully fetched HTML content from: {url}")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Could not fetch URL: {url} - {e}")
        return None


def extract_hacker_news_links(html, max_links=5):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    seen = set()
    for item in soup.select(".titleline > a"):
        url = item["href"]
        title = item.text.strip()
        if url.startswith("item?id="):
            url = f"https://news.ycombinator.com/{url}"
        if url not in seen and title:
            links.append({"url": url, "text": title})
            seen.add(url)
        if len(links) >= max_links:
            break
    print(f"Extracted {len(links)} links from Hacker News.")
    return links


def extract_github_trending(html, max_links=5):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for repo in soup.select("article.Box-row h2 a"):
        url = f"https://github.com{repo['href']}"
        title = re.sub(r"\s+", " ", repo.text).strip()
        if title and url:
            links.append({"url": url, "text": title})
        if len(links) >= max_links:
            break
    print(f"Extracted {len(links)} trending repositories from GitHub.")
    return links


def call_mistral_api(prompt, model="mistral-small-latest"):
    api_key = MISTRAL_API_KEY
    if not api_key:
        print("Error: MISTRAL_API_KEY environment variable not set.")
        return None

    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    data = {"model": model, "messages": [{"role": "user", "content": prompt}]}

    try:
        print(f"Calling Mistral API with model: {model}")
        print(f"Prompt being sent: {prompt[:1000]}...")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        print(f"Mistral API Response: {response_json}")
        if response_json and response_json.get("choices"):
            content = response_json["choices"][0]["message"]["content"]
            print(f"Mistral API Content: {content}")
            return content
        else:
            print(f"Mistral API Error: Invalid response format: {response_json}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Mistral API Error: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        return None


def fetch_and_summarize(url, fallback_title=None):
    print(f"Summarizing: {url}")
    html = fetch_html_content(url)
    if not html:
        return {
            "url": url,
            "summary": "Could not fetch content.",
            "title": fallback_title or url,
        }
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text.strip() if soup.title else (fallback_title or url)
    paragraphs = soup.find_all("p")
    text_content = "\n".join(p.get_text() for p in paragraphs)
    if not text_content or len(text_content) < 100:
        text_content = soup.get_text(separator="\n")
    text_content = text_content.strip()
    if len(text_content) > 3000:
        text_content = text_content[:3000]
    summary = ai_summarize(text_content, url, title)
    return {"url": url, "summary": summary, "title": title}


def limit_to_n_words(text, n):
    words = text.strip().split()
    if len(words) <= n:
        return text.strip()
    return " ".join(words[:n]) + "..."


def ai_summarize(text, url=None, title=None):
    if not MISTRAL_API_KEY:
        print("No MISTRAL_API_KEY set. Returning first 15 words as summary.")
        return limit_to_n_words(text, 15)
    prompt = (
        "If the original text is in Chinese, summarize it in English. "
        "Summarize the following web page content in clear, concise English. "
        "Focus on the single most important point or insight. "
        "Your summary should be around 300 characters. "
        "Output only the summary sentence:\n"
        f"Title: {title if title else ''}\n"
        f"{text}\n"
        f"{'Original link: ' + url if url else ''}"
    )
    summary = call_mistral_api(prompt)
    if summary is None:
        return limit_to_n_words(text, 15)
    return summary.strip()[:300]


def generate_summarized_report(summaries, source_name):
    text = f"{source_name}\n"
    text += "-" * len(source_name) + "\n"
    if not summaries:
        text += "No items found.\n\n"
        return text
    url_pattern = re.compile(r"(https?://[^\s]+)")
    for idx, item in enumerate(summaries, 1):
        summary = item.get("summary", "").replace("\n", " ").replace("\r", " ").strip()
        summary = summary.replace("*", "")
        summary = url_pattern.sub("", summary)
        summary = summary[:300]
        text += f"{idx}. {summary}\n\n"
    text += "\n"
    return text


def extract_nytimes_links(html, max_links=5):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        url = a["href"]
        if url.startswith("https://cn.nytimes.com/"):
            links.append({"url": url, "text": a.text.strip()})
        if len(links) >= max_links:
            break
    print(f"Extracted {len(links)} links from main page.")
    return links


def summarize_nytimes_article(url):
    html = fetch_html_content(url)
    if not html:
        return {"url": url, "summary": "Could not fetch content.", "title": url}
    soup = BeautifulSoup(html, "html.parser")
    title_element = soup.select_one(
        ".article-area .article-content .article-header header h1"
    )
    title = (
        title_element.text.strip()
        if title_element
        else (soup.title.text.strip() if soup.title else url)
    )
    article_area = soup.find("section", class_="article-body")
    if article_area:
        article_text = article_area.get_text(separator="\n", strip=True)
    else:
        article_text = soup.get_text(separator="\n", strip=True)
    if not article_text or len(article_text) < 100:
        article_text = soup.get_text(separator="\n", strip=True)
    if len(article_text) > 3000:
        article_text = article_text[:3000]
    summary = ai_summarize(article_text, url, title)
    return {"url": url, "summary": summary, "title": title}
